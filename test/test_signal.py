import pandas as pd
from sympy import Point2D

from src.wifi.signal import Signal


def test_signal_to_dataframe():
    expected = pd.DataFrame(data=
    {
        'location': [[1, 1]], 'signal_strength': [1], 'sniff_timestamp': [1567757309]
    })

    signal = Signal(Point2D(1, 1), 1, 1567757309)

    actual = signal.to_dataframe()

    pd.testing.assert_frame_equal(actual, expected)
