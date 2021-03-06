from types import FunctionType

from src.device.device import Device
from src.device.device_aggregator import device_aggregator
from src.wifi.frame_control_information import FrameControlInformation
from src.wifi.signal import Signal
from src.wifi.wifi_frame import WifiFrame
from src.wifi.wlan_radio_information import WlanRadioInformation

address_for_test_1 = "00:00:00:00:00:01"
address_for_test_2 = "00:00:00:00:00:03"
address_for_test_3 = "00:00:00:00:00:03"


def make_device(address, number_of_frames, receiver_address=None, sniff_timestamp=1):
    return Device(address, [
        WifiFrame(frame_control_information=
                  FrameControlInformation(transmitter_address=address, receiver_address=receiver_address),
                  wlan_radio=
                  WlanRadioInformation([Signal(None, None, sniff_timestamp)]))
        for _ in range(number_of_frames)
    ])


def get_receiver_address(frame: WifiFrame):
    return frame.frame_control_information.receiver_address


def true_for_all_frames(device: Device, test: FunctionType):
    return all(test(frame) for frame in device.frames)


def get_signals(frame: WifiFrame):
    return frame.wlan_radio.signals


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


def test_device_aggregator_removes_frames_from_buffer_if_over_max():
    devices = [
        make_device(address_for_test_1, 1, "0"),
        make_device(address_for_test_1, 1, "1"),
        make_device(address_for_test_1, 1, "2"),
        make_device(address_for_test_1, 1, "3")
    ]

    aggregated_devices = list(device_aggregator(devices, max_frame_buffer_size=2))

    assert len(aggregated_devices[0].frames) == 2
    assert get_receiver_address(aggregated_devices[0].frames[0]) == "2"
    assert get_receiver_address(aggregated_devices[0].frames[1]) == "3"


def test_device_aggregator_given_device_does_not_set_timestamp_delta():
    devices = [
        make_device(address_for_test_1, 1)
    ]

    first_device = list(device_aggregator(devices))[0]

    # This is a somewhat complex assertion due to the nested structure of the WifiFrame class
    assert true_for_all_frames(first_device, lambda frame: get_signals(frame)[0].timestamp_delta == None)


def test_device_aggregator_given_device_and_previous_frames_sets_timestamp_delta_on_new_frames():
    devices = [
        make_device(address_for_test_1, 1, "0", 10),
        make_device(address_for_test_1, 1, "1", 14),
    ]

    first_device = list(device_aggregator(devices))[0]
    first_frame = first_device.frames[0]
    second_frame = first_device.frames[1]

    assert get_signals(first_frame)[0].timestamp_delta == None
    assert get_signals(second_frame)[0].timestamp_delta == 4
