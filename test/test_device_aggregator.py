import pytest

from src.device.device_aggregator import device_aggregator
from src.device.device import Device
from src.wifi.wifi_frame import WifiFrame
from src.wifi.frame_control_information import FrameControlInformation

address_for_test_1 = "00:00:00:00:00:01"
address_for_test_2 = "00:00:00:00:00:03"
address_for_test_3 = "00:00:00:00:00:03"


def make_device(address, number_of_frames, receiver_address=None):
    return Device(address, [
        WifiFrame(frame_control_information=
                  FrameControlInformation(transmitter_address=address, receiver_address=receiver_address))
        for _ in range(number_of_frames)
    ])


def get_receiver_address(frame: WifiFrame):
    return frame.frame_control_information.receiver_address


def test_device_aggregator_given_device_added_to_list():
    devices = [
        make_device(address_for_test_1, 1)
    ]

    aggregated_devices = list(device_aggregator(devices))

    assert len(aggregated_devices) == 1
    assert aggregated_devices[0] == devices[0]


def test_device_aggregator_given_devices_added_to_list():
    devices = [
        make_device(address_for_test_1, 1),
        make_device(address_for_test_2, 1)
    ]

    aggregated_devices = list(device_aggregator(devices))

    assert len(aggregated_devices) == 2
    assert aggregated_devices[0] == devices[0]
    assert aggregated_devices[1] == devices[1]


def test_device_aggregator_given_device_updates_previously_given_device():
    devices = [
        make_device(address_for_test_1, 1, "0"),
        make_device(address_for_test_1, 1, "1"),
    ]

    aggregated_devices = list(device_aggregator(devices))

    assert len(aggregated_devices) == 2
    assert len(aggregated_devices[0].frames) == 2
    assert get_receiver_address(aggregated_devices[0].frames[0]) == "0"
    assert get_receiver_address(aggregated_devices[0].frames[1]) == "1"


def test_device_aggregator_given_device_updates_previously_given_device_with_all_frames():
    devices = [
        make_device(address_for_test_1, 1, "0"),
        make_device(address_for_test_1, 2, "1")
    ]

    aggregated_devices = list(device_aggregator(devices))

    assert len(aggregated_devices) == 2
    assert len(aggregated_devices[0].frames) == 3
    assert get_receiver_address(aggregated_devices[0].frames[0]) == "0"
    assert get_receiver_address(aggregated_devices[0].frames[1]) == "1"
    assert get_receiver_address(aggregated_devices[0].frames[2]) == "1"


def test_device_aggregator_given_device_updates_first_device_given():
    devices = [
        make_device(address_for_test_1, 1, "0"),
        make_device(address_for_test_2, 1, "1"),
        make_device(address_for_test_1, 1, "2")
    ]

    aggregated_devices = list(device_aggregator(devices))

    assert len(aggregated_devices) == 3
    assert len(aggregated_devices[0].frames) == 2
    assert get_receiver_address(aggregated_devices[0].frames[0]) == "0"
    assert get_receiver_address(aggregated_devices[0].frames[1]) == "2"
