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
        Signal(Point2D(0, 1), -20, 0, variance=1),
        Signal(Point2D(1, 0), -20, 0, variance=1),
    ])

    calculate_position(device, 4)

    # Numbers verified with do_draw=True
    assert device.position == pytest.approx([7.392051109661893, 7.3920437313842])


def test_calculate_position_from_device_with_identification():
    device = Device(address_for_test, [
        WifiFrame(wlan_radio=WlanRadioInformation(frequency_mhz=2412))
    ],
                    identification=['10'],
                    averaged_signals=[
                        Signal(Point2D(0, 0), -20, 0, variance=1),
                        Signal(Point2D(0, 1), -20, 0, variance=1),
                        Signal(Point2D(1, 0), -20, 0, variance=1),
                    ])

    calculate_position(device, 4)

    # Numbers verified with do_draw=True
    assert device.position == pytest.approx([4.286877918320265, 4.2868779517285])
