from typing import Iterable

from src.device.device import Device


def device_aggregator(generator: Iterable[Device], max_frame_buffer_size=50):
    known_devices = {}

    for new_device in generator:
        if new_device in known_devices:
            known_devices[new_device].frames.extend(new_device.frames)
            while len(known_devices[new_device].frames) > max_frame_buffer_size:
                known_devices[new_device].frames.pop(0)
        else:
            known_devices[new_device] = new_device

        yield known_devices[new_device]
