import pandas as pd
from sympy import Point2D

from src.wifi.signal import Signal

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