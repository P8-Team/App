import pytest
from src.device.device import Device
from src.wifi.wifi_frame import WifiFrame
from src.wifi.frame_control_information import FrameControlInformation
from sympy import Point2D

address_for_test = "00:00:00:00:00:01"


def test_device_uses_given_physical_address():
    device = Device(address_for_test, [])

    assert device.physical_address == address_for_test


def test_device_uses_given_list_of_wifi_frames():
    wifi_frame = WifiFrame()
    device = Device(address_for_test, [wifi_frame])

    assert device.frames[0] == wifi_frame


def test_device_uses_given_identification():
    identification = 1
    device = Device(address_for_test, [], identification=identification)

    assert device.identification == identification


def test_device_uses_given_position():
    position = Point2D(1, 5)
    device = Device(address_for_test, [], position=position)

    assert device.position == position


def test_device_from_frame_returns_device_with_physical_address_and_frame():
    wifi_frame = WifiFrame(frame_control_information=FrameControlInformation(transmitter_address=address_for_test))

    device = Device.from_frame(wifi_frame)

    assert device.physical_address == address_for_test
    assert device.frames[0] == wifi_frame
