from sympy import Point2D

from src.wifi.frame_control_information import FrameControlInformation
from src.wifi.signal import Signal
from src.wifi.wifi_frame import WifiFrame
from src.wifi.wlan_radio_information import WlanRadioInformation


def frame_factory(timestamp: float, location=None):
    if location is None:
        location = Point2D([0, 0])
    return WifiFrame(
        100,
        WlanRadioInformation(
            signals=[Signal(location, -40, timestamp)],
            frequency_mhz=2412,
        ),
        FrameControlInformation(
            transmitter_address="00:00:00:00:00:01",
            receiver_address="00:00:00:00:00:02",
            fc_type=1,
            subtype=1,
        ),
    )
