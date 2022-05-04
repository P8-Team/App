import uuid

from sympy import Point2D

from src.wifi.frame_control_information import FrameControlInformation
from src.wifi.signal import Signal
from src.wifi.wifi_frame import WifiFrame
from src.wifi.wlan_radio_information import WlanRadioInformation


def frame_factory(timestamp: float, location=None, signal_strength=-40, frame_control_sequence=None):
    if location is None:
        location = Point2D([0, 0])
    # Create signal with timedelta
    timestamp_delta = 10
    signal = Signal(location, signal_strength, timestamp)
    signal.timestamp_delta = timestamp_delta
    return WifiFrame(
        100,
        frame_control_sequence if frame_control_sequence is not None else uuid.uuid4().int,
        WlanRadioInformation(
            signals=[signal],
            frequency_mhz=2412,
        ),
        FrameControlInformation(
            transmitter_address="00:00:00:00:00:01",
            receiver_address="00:00:00:00:00:02",
            fc_type=1,
            subtype=1,
        ),
    )
