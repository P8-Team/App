from typing import Iterable

from src.device.device import Device
from src.wifi.wifi_frame import WifiFrame


def frame_to_device_converter(generator: Iterable[WifiFrame]):
    for frame in generator:
        yield Device.from_frame(frame)
