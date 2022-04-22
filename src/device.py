from typing import Iterator

from sympy import Point2D

from src.wifi.wifi_frame import WifiFrame


class Device:

    def __init__(self, physical_address: str, wifi_frames: list[WifiFrame],
                 identification=None, position: Point2D = None):

        self.physical_address = physical_address
        self.frames = wifi_frames
        self.identification = identification
        self.position = position
