from sympy import Point2D


class Signal:
    location: Point2D
    signal_strength: float
    sniff_timestamp: float

    def __init__(self, location: Point2D, signal_strength:  float, sniff_timestamp: float):
        self.location = location
        self.signal_strength = signal_strength
        self.sniff_timestamp = sniff_timestamp
