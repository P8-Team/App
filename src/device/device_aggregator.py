from typing import Iterator
from src.device.device import Device


def device_aggregator(generator: Iterator[Device]):
    known_devices = {}

    for new_device in generator:
        if new_device in known_devices:
            known_devices[new_device].frames.extend(new_device.frames)
        else:
            known_devices[new_device] = new_device

        yield known_devices[new_device]
