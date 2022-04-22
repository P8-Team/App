from src.location.average_signal_strength_aggregator import generate_average_signal_strength
from test.utils.wifi_frame_factory import frame_factory


def test_it_calculates_rolling_average():
    # Given 10 wifi frames in a generator, it should produce 10 averages of the signal strength
    # in a rolling window of 5 frames.
    wifi_frames = [
        frame_factory(0, signal_strength=10),
        frame_factory(0, signal_strength=20),
        frame_factory(0, signal_strength=30),
        frame_factory(0, signal_strength=40),
        frame_factory(0, signal_strength=50),
        frame_factory(0, signal_strength=60),
        frame_factory(0, signal_strength=70),
        frame_factory(0, signal_strength=80),
        frame_factory(0, signal_strength=90),
        frame_factory(0, signal_strength=100),
    ]

    result = generate_average_signal_strength(wifi_frames, 5)

    # convert to list
    result = list(result)
    signal_strengths = [wifi_frame.wlan_radio.signals[0].signal_strength for wifi_frame in result]

    assert signal_strengths == [
        10, 15, 20, 25, 30, 40, 50, 60, 70, 80
    ]


def test_it_calculates_rolling_variance():
    # Given 10 wifi frames in a generator, it should produce 10 averages of the signal strength
    # in a rolling window of 5 frames.
    wifi_frames = [
        frame_factory(0, signal_strength=20),
        frame_factory(0, signal_strength=20),
        frame_factory(0, signal_strength=20),
        frame_factory(0, signal_strength=20),
        frame_factory(0, signal_strength=20),
        frame_factory(0, signal_strength=60),
        frame_factory(0, signal_strength=20),
        frame_factory(0, signal_strength=20),
        frame_factory(0, signal_strength=20),
        frame_factory(0, signal_strength=100),
    ]

    result = generate_average_signal_strength(wifi_frames, 5)

    # convert to list
    result = list(result)
    variances = [wifi_frame.wlan_radio.signals[0].variance for wifi_frame in result]

    assert variances == [
        0, 0, 0, 0, 0, 16, 16, 16, 16, 32
    ]

