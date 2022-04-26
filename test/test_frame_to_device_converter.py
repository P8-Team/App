from src.device.frame_to_device_converter import frame_to_device_converter
from src.wifi.frame_control_information import FrameControlInformation
from src.wifi.wifi_frame import WifiFrame

address_for_test_1 = "00:00:00:00:00:01"
address_for_test_2 = "00:00:00:00:00:02"


def make_wifi_frame(physical_address):
    return WifiFrame(frame_control_information=FrameControlInformation(transmitter_address=physical_address))


def test_frame_to_device_converter_returns_device_with_given_physical_address():
    wifi_frame = make_wifi_frame(address_for_test_1)
    devices = list(frame_to_device_converter([wifi_frame]))

    assert len(devices) == 1
    assert devices[0].physical_address == address_for_test_1


def test_frame_to_device_converter_returns_device_with_given_frame():
    wifi_frame = make_wifi_frame(address_for_test_1)

    devices = list(frame_to_device_converter([wifi_frame]))

    assert len(devices) == 1
    assert len(devices[0].frames) == 1
    assert devices[0].frames[0] == wifi_frame


def test_frame_to_device_converter_converts_multiple_physical_addresses_to_multiple_devices():
    frames = [
        make_wifi_frame(address_for_test_1),
        make_wifi_frame(address_for_test_2)
    ]

    devices = list(frame_to_device_converter(frames))

    assert len(devices) == 2
