from time import sleep

from iterators import TimeoutIterator
from sympy import Point2D

from src.frame_aggregator import frame_aggregator, frame_aggregator_sniff_timestamp
from src.wifi.frame_control_information import FrameControlInformation
from src.wifi.signal import Signal
from src.wifi.wifi_frame import WifiFrame
from src.wifi.wlan_radio_information import WlanRadioInformation


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
            signals=[Signal(Point2D([0, 0]), signal_strength, sniff_timestamp)],
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
    assert combined_frame.wlan_radio.signals[0].sniff_timestamp == 1
    assert combined_frame.wlan_radio.signals[1].sniff_timestamp == 2
    assert combined_frame.wlan_radio.signals[2].sniff_timestamp == 3
    assert combined_frame.wlan_radio.signals[0].signal_strength == 5
    assert combined_frame.wlan_radio.signals[1].signal_strength == 6
    assert combined_frame.wlan_radio.signals[2].signal_strength == 7

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


def test_frame_aggregator_with_sniff_timestamp_not_exceeding_threshold():
    # Arrange
    frames = [
        make_wifi_frame(1, 5),
        make_wifi_frame(1, 6),
    ]

    # Act
    combined_frames = list(frame_aggregator_sniff_timestamp(iter(frames), 3, 1))

    # Assert
    assert len(combined_frames) == 0


def test_frame_aggregator_with_sniff_timestamp_getting_earlier_sniff_timestamp_than_previous():
    # Arrange
    frames = [
        make_wifi_frame(2, 5),
        make_wifi_frame(1, 6),
        make_wifi_frame(0, 6),
    ]

    # Act
    combined_frames = list(frame_aggregator_sniff_timestamp(iter(frames), 3, 1))

    # Assert
    assert len(combined_frames) == 1
    assert len(combined_frames[0].wlan_radio.signals) == 3


def test_frame_aggregator_with_sniff_timestamp_expire():
    # Arrange
    frames = [
        make_wifi_frame(2, 5),
        make_wifi_frame(3, 6),
        make_wifi_frame(8, 6),
    ]

    # Act
    combined_frames = list(frame_aggregator_sniff_timestamp(iter(frames), 3, 1))

    # Assert
    assert len(combined_frames) == 0


def test_frame_aggregator_with_sniff_timestamp_exceeding_threshold():
    # Arrange
    frames = [
        make_wifi_frame(2, 5),
        make_wifi_frame(2.1, 6),
        make_wifi_frame(2.2, 6),
    ]

    # Act
    combined_frames = list(frame_aggregator_sniff_timestamp(iter(frames), 3, 1))

    # Assert
    assert len(combined_frames) == 1
    assert len(combined_frames[0].wlan_radio.signals) == 3


def test_frame_aggregator_with_sniff_timestamp_default_parameters():
    # Arrange
    frames = [
        make_wifi_frame(2, 5),
        make_wifi_frame(3.1, 6),
        make_wifi_frame(2.2, 6),
    ]

    # Act
    combined_frames = list(frame_aggregator_sniff_timestamp(iter(frames)))

    # Assert
    assert len(combined_frames) == 1
    assert len(combined_frames[0].wlan_radio.signals) == 3
