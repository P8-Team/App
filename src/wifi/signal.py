from __future__ import annotations

import pandas as pd
from sympy import Point2D


class Signal:
    location: Point2D
    signal_strength: float
    sniff_timestamp: float
    variance: float

    def __init__(self, location: Point2D, signal_strength: float, sniff_timestamp: float, variance=None):
        self.location = location
        self.signal_strength = signal_strength
        self.sniff_timestamp = sniff_timestamp
        self.variance = variance
        self.timestamp_delta = None

    def to_dataframe(self):
        return pd.DataFrame(data={
            'signal_strength': [self.signal_strength], 'sniff_timestamp': [self.sniff_timestamp]
        })

    def set_timestamp_delta_from_other_signal(self, other: Signal):
        self.timestamp_delta = self.sniff_timestamp_delta(other, self)

    @staticmethod
    def sniff_timestamp_delta(old_signal: Signal, new_signal: Signal):
        return new_signal.sniff_timestamp - old_signal.sniff_timestamp