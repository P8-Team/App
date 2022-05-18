from typing import Iterable

from src.device.device import Device


class Oracle:

    def __init__(self, device_address_dict: dict):
        self.device_list = device_address_dict

    def classify(self, generator: Iterable[Device]):
        for device in generator:
            if device.identification is None and device.physical_address in self.device_list:
                device.identification = self.device_list[device.physical_address]

            yield device
