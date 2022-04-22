import math

from sympy import Point

from src.wifi.signal import Signal
from src.device.device import Device


def calculate_average_signal_strength(device: Device):
    signal_strengths = []

    for frame in device.frames:
        signal_strengths.append(frame.wlan_radio.signals)

    device.averaged_signals = average_signals(signal_strengths)


def average_signals(signals: list[list[Signal]]) -> list[Signal]:
    last_element = signals[-1]
    avg_signals = []
    for signal_location in last_element:
        average, variance = average_and_variance_from_signal_strength_on_location(signals, signal_location.location)
        signal = Signal(signal_location.location, average, signal_location.sniff_timestamp)
        signal.variance = variance
        avg_signals.append(signal)
    return avg_signals


def average_and_variance_from_signal_strength_on_location(signals: list[list[Signal]], location: Point) \
        -> tuple[float, float]:
    signal_strengths = []
    for signal_group in signals:
        for signal in signal_group:
            if signal.location == location:
                signal_strengths.append(signal.signal_strength)

    average = sum(signal_strengths) / len(signal_strengths)
    variance = math.sqrt(
        sum([math.pow(signal_strength - average, 2) for signal_strength in signal_strengths]) / len(signal_strengths)
    )

    return average, variance
