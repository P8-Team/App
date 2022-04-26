import math
from typing import Iterator

from sympy import Point

from src.wifi.signal import Signal
from src.wifi.wifi_frame import WifiFrame


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


def average_signals(signals: list[list[Signal]]) -> list[Signal]:
    last_element = signals[-1]
    avg_signals = []
    for signal_location in last_element:
        average, variance = average_and_variance_from_signal_strength_on_location(signals, signal_location.location)
        signal = Signal(signal_location.location, average, signal_location.sniff_timestamp)
        signal.variance = variance
        avg_signals.append(signal)
    return avg_signals


def generate_average_signal_strength(wifi_frame_generator: Iterator[WifiFrame],
                                     max_rolling_window_size: int) -> Iterator[WifiFrame]:
    # Keep a mapping from MAC address to a window of rolling recent signal strengths
    signal_strength_windows = {}

    for frame in wifi_frame_generator:
        mac_address = frame.frame_control_information.transmitter_address
        signals = frame.wlan_radio.signals
        # If mac address already exist

        if mac_address in signal_strength_windows:
            # If the window is full, remove the oldest signal strength
            if len(signal_strength_windows[mac_address]) == max_rolling_window_size:
                signal_strength_windows[mac_address].pop(0)
            # Add the new signal strength to the window
            signal_strength_windows[mac_address].append(signals)
        else:
            signal_strength_windows[mac_address] = [signals]

        frame.wlan_radio.signals = average_signals(signal_strength_windows[mac_address])

        yield frame
