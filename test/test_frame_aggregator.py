from time import sleep

from iterators import TimeoutIterator

from src.frame_aggregator import frame_aggregator
from src.frame_control_information import FrameControlInformation
from src.wifi_frame import WifiFrame
from src.wlan_radio_information import WlanRadioInformation


def make_wifi_frame(sniff_timestamp, signal_strength, transmitter_address='00:00:00:00:00:01'):
    return WifiFrame(
        length=200,
        frame_control_information=FrameControlInformation(
            fc_type=0,
            subtype=1,
            receiver_address='00:00:00:00:00:00',
            transmitter_address=transmitter_address,
        ),
        wlan_radio=WlanRadioInformation(
            signals = [{'signal_strength': signal_strength, 'sniff_timestamp': sniff_timestamp}],
            data_rate=12,
            radio_timestamp=1200
        )
    )


def test_frame_aggregator_combine_frames():
    # Arrange
    frames = [
        make_wifi_frame(1, 5),
        make_wifi_frame(2, 6),
        make_wifi_frame(3, 7),
    ]

    # Act
    combined_frames = list(frame_aggregator(frames, 3, 1, 10))

    # Assert
    assert len(combined_frames) == 1
    combined_frame = combined_frames[0]
    assert len(combined_frame.wlan_radio.signals) == 3
    assert combined_frame.wlan_radio.signals[0]['sniff_timestamp'] == 1
    assert combined_frame.wlan_radio.signals[1]['sniff_timestamp'] == 2
    assert combined_frame.wlan_radio.signals[2]['sniff_timestamp'] == 3
    assert combined_frame.wlan_radio.signals[0]['signal_strength'] == 5
    assert combined_frame.wlan_radio.signals[1]['signal_strength'] == 6
    assert combined_frame.wlan_radio.signals[2]['signal_strength'] == 7

    # Rest of the combined frame should be equal to any of the test input frames
    # as the compare function does not care about signal_strength or sniff_timestamp
    assert combined_frame == frames[0]


def test_frame_aggregator_threshold_one():
    # Arrange
    frames = [
        make_wifi_frame(1, 5),
    ]

    # Act
    combined_frames = list(frame_aggregator(frames, 1, 0.1, 10))

    # Assert
    assert len(combined_frames) == 1


def test_frame_aggregator_does_not_yield_frames_before_threshold_reached():
    # Arrange
    frames = [
        make_wifi_frame(1, 5),
        make_wifi_frame(2, 6),
        make_wifi_frame(3, 7),
    ]

    # Act
    combined_frames = list(frame_aggregator(frames, 4, 2, 10))

    # Assert
    assert len(combined_frames) == 0


def test_frame_aggregator_frames_expire():
    """
        The idea of this test, is to provide the aggregator with enough frames to exceed the threshold,
        and combine them into a combined frame.

        However the generator is slow (sleeps 0.05 seconds pr frame), such that the aggregator does not see the
        required frames in time, and therefore drops the combined frame.

        The use case for this, is to automatically disregard old frames, as there will always be a chance for a
        wifi frame to only reach a subset of the threshold. Without the expiry, the aggregator would never drop
        the frames from the buffer, essentially creating an ever growing buffer.
    """

    # Arrange
    frames = [
        make_wifi_frame(1, 5),
        make_wifi_frame(2, 6),
        make_wifi_frame(3, 7),
    ]

    def slow_generator(list_of_frames):
        for frame in list_of_frames:
            sleep(0.05)
            yield frame

    # Act
    combined_frames = list(TimeoutIterator(frame_aggregator(slow_generator(frames), 3, 0.1, 10), 0.2))

    # Assert
    assert len(combined_frames) == 0


def test_frame_aggregator_full_buffer():
    # Arrange
    frames = [
        make_wifi_frame(1, 5),
        make_wifi_frame(2, 6),

        # Fill the buffer with other frames.
        make_wifi_frame(4, 5, transmitter_address='00:00:00:00:00:03'),
        make_wifi_frame(5, 6, transmitter_address='00:00:00:00:00:04'),
        make_wifi_frame(5, 6, transmitter_address='00:00:00:00:00:05'),

        # This would result in a combined frame, if the first two frames is still in the buffer.
        make_wifi_frame(3, 7),
    ]

    # Act
    combined_frames = list(frame_aggregator(frames, 3, 1, 2))

    # Assert that the first two frames were dropped
    assert len(combined_frames) == 0
