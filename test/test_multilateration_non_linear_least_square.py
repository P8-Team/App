import pytest
from sympy import Point2D

from src.device.device import Device
from src.location.multi_lateration_non_linear_least_square_sum import calculate_position
from src.wifi.signal import Signal
from src.wifi.wifi_frame import WifiFrame
from src.wifi.wlan_radio_information import WlanRadioInformation

address_for_test = "00:00:00:00:00:01"


def test_calculate_position_from_device():
    device = Device(address_for_test, [
        WifiFrame(wlan_radio=WlanRadioInformation(frequency_mhz=2412))
    ], averaged_signals=[
        Signal(Point2D(0, 0), -20, 0, variance=1),
        Signal(Point2D(0, 1), -22, 0, variance=1),
        Signal(Point2D(1, 0), -23, 0, variance=1),
    ])

    calculate_position(device)

    assert device.position == pytest.approx([0.8389631665687186, 0.7858192567441246])


def test_calculate_position_from_device_with_identification():
    #     device = Device(address_for_test, [
    #         WifiFrame(wlan_radio=WlanRadioInformation(frequency_mhz=2412))
    #     ],
    #                     identification={"transmission_power_dbm": 10},
    #                     averaged_signals=[
    #                         Signal(Point2D(0, 0), -22, 0, variance=1),
    #                         Signal(Point2D(0, 1), -28, 0, variance=1),
    #                         Signal(Point2D(1, 0), -28, 0, variance=1),
    #                     ])
    device = Device(address_for_test, [
        WifiFrame(wlan_radio=WlanRadioInformation(frequency_mhz=2412))
    ],
                    identification={"transmission_power_dbm": 10},
                    averaged_signals=[
                        Signal(Point2D(0, 0), -42, 0, variance=1),
                        Signal(Point2D(0, 1), -45, 0, variance=1),
                        Signal(Point2D(1, 0), -40, 0, variance=1),
                    ])

    calculate_position(device, do_draw=True)

    assert device.position == pytest.approx([0.22825998907501197, 0.3350799415348499])
