import pandas as pd
from sympy import Point2D

from src.wifi.signal import Signal


def test_signal_to_dataframe_with_timestamp_delta():
    expected = pd.DataFrame(data=
    {
        'signal_strength': [1], 'timestamp_delta': [111]
    })

    signal = Signal(Point2D(1, 1), 1, 1567757309)
    signal.timestamp_delta = 111

    actual = signal.to_dataframe()

    pd.testing.assert_frame_equal(actual, expected)

def test_signal_to_dataframe_without_timestamp_delta():
    expected = pd.DataFrame(data=
    {
        'signal_strength': [1], 'timestamp_delta': [None]
    })

    signal = Signal(Point2D(1, 1), 1, 1567757309)

    actual = signal.to_dataframe()

    pd.testing.assert_frame_equal(actual, expected)

def test_sniff_timestamp_delta():
    signal1 = Signal(Point2D(1, 1), 1, 100)
    signal2 = Signal(Point2D(1, 1), 1, 110)

    assert Signal.sniff_timestamp_delta(signal1, signal2) == 10
    assert Signal.sniff_timestamp_delta(signal2, signal1) == -10

def test_timestamp_delta_is_initially_none():
    signal = Signal(Point2D(1, 1), 1, 100)

    assert signal.timestamp_delta == None

def test_timestamp_delta_from_other_signal():
    signal1 = Signal(Point2D(1, 1), 1, 100)
    signal2 = Signal(Point2D(1, 1), 1, 105.5)

    signal2.set_timestamp_delta_from_other_signal(signal1)

    assert signal2.timestamp_delta == 5.5

    signal1.set_timestamp_delta_from_other_signal(signal2)

    assert signal1.timestamp_delta == -5.5