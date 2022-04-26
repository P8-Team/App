from __future__ import annotations

from sympy import Point2D

from src.wifi.signal import Signal
from src.wifi.wifi_frame import WifiFrame


class Device:
    """
    Data structure for keeping track of a device and its Wi-Fi frames
    """

    def __init__(self, physical_address: str, wifi_frames: [WifiFrame],
                 identification=None, position: Point2D = None, averaged_signals: [Signal] = None):
        self.physical_address = physical_address
        self.frames = wifi_frames
        self.identification = identification
        self.position = position
        self.averaged_signals = averaged_signals
        self.historic_positions = []

    @classmethod
    def from_frame(cls, frame: WifiFrame):
        return cls(frame.frame_control_information.transmitter_address, [frame])

    def set_position(self, new_position):
        if self.position is not None:
            self.historic_positions.append(self.position)

        self.position = new_position

    def __eq__(self, physical_address: str) -> bool:
        return self.physical_address == physical_address

    def __hash__(self):
        return hash(self.physical_address)

    def __repr__(self) -> str:
        return f"{self.frames[-1].wlan_radio.radio_timestamp} - {self.physical_address}: " \
               f"identification={self.identification}, " \
               f"position=({self.position.x}, {self.position.y}), " \
               f"distance={self.position.distance(Point2D([0, 0]))}"
