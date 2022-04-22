from typing import Iterator
from src.wifi.wifi_frame import WifiFrame
from src.device.device import Device


def frame_to_device_converter(generator: Iterator[WifiFrame]):
    for frame in generator:
        yield Device.from_frame(frame)
