from sympy import Point2D
import pandas as pd

class Signal:
    location: Point2D
    signal_strength: float
    sniff_timestamp: float

    def __init__(self, location: Point2D, signal_strength:  float, sniff_timestamp: float):
        self.location = location
        self.signal_strength = signal_strength
        self.sniff_timestamp = sniff_timestamp

    def to_dataframe(self):
        return pd.DataFrame(data = {
         'location': [[self.location.x,self.location.y]], 'signal_strength': [self.signal_strength], 'sniff_timestamp': [self.sniff_timestamp]
        })