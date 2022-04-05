from src.frame_control_information import FrameControlInformation
from src.wifi_frame import WifiFrame
from src.wlan_radio_information import WlanRadioInformation


def frame_factory(timestamp, location=None):
    if location is None:
        location = [0, 0]
    return WifiFrame(
        100,
        WlanRadioInformation(
            signals=[{'signal_strength': -40, 'location': location, 'sniff_timestamp': timestamp}],
            frequency_mhz=2412,
        ),
        FrameControlInformation(
            transmitter_address="00:00:00:00:00:01",
            receiver_address="00:00:00:00:00:02",
            fc_type=1,
            subtype=1,
        ),
    )