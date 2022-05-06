from typing import Iterable

from src.device.device import Device
from src.wifi.wifi_frame import WifiFrame


def device_aggregator(generator: Iterable[Device], max_frame_buffer_size=50):
    """
    Merges devices from the pipeline based on their physical addresses
    (the same physical addresses are merged to the same device).
    Any new Wi-Fi frames are added to the device's list of frames
    """

    known_devices = {}

    for new_device in generator:
        if new_device in known_devices:
            known_devices[new_device].frames.extend(new_device.frames)
            while len(known_devices[new_device].frames) > max_frame_buffer_size:
                known_devices[new_device].frames.pop(0)
        else:
            known_devices[new_device] = new_device
        __set_timestamp_deltas(known_devices[new_device].frames)
        yield known_devices[new_device]

def __set_timestamp_deltas(frames: list[WifiFrame]):
    # Given list [1,2,3,4], this loop creates two new lists
    # [1,2,3]
    # [2,3,4]
    # These are then combined using zip into a single list of tuples 
    # [(1,2), (2,3), (3,4)]
    for old_frame, new_frame in zip(frames[:-1], frames[1:]):
        old_signals = old_frame.wlan_radio.signals
        new_signals = new_frame.wlan_radio.signals
        # Calculate the timestamp_delta for each signal
        # This assumes that there are the same number of signals
        for old_signal, new_signal in zip(old_signals, new_signals):
            new_signal.set_timestamp_delta_from_other_signal(old_signal)