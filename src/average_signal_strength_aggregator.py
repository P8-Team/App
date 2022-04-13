from typing import Generator

from sympy import Point

from src.wifi.signal import Signal
from src.wifi.wifi_frame import WifiFrame


def average_signal_strength_on_location(signals: list[list[Signal]], location: Point) -> float:
    signal_strengths = []
    for signalGroup in signals:
        for signal in signalGroup:
            if signal.location == location:
                signal_strengths.append(signal.signal_strength)
    return sum(signal_strengths) / len(signal_strengths)


def average_signals(signals: list[list[Signal]]) -> list[Signal]:
    last_element = signals[-1]
    average_signals = []
    for signal_location in last_element:
        average_signals.append(
            Signal(signal_location.location, average_signal_strength_on_location(signals, signal_location.location),
                   signal_location.sniff_timestamp))
    return average_signals


def generate_average_signal_strength(wifi_frame_generator: Generator[WifiFrame, None, None],
                                     max_rolling_window_size: int) -> Generator[WifiFrame, None, None]:
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
