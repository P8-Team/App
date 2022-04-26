from src.location.average_signal_strength import calculate_average_signal_strength
from test.utils.wifi_frame_factory import frame_factory
from src.device.device import Device
from src.wifi.wifi_frame import WifiFrame
from src.wifi.wlan_radio_information import WlanRadioInformation
from src.wifi.signal import Signal
from sympy import Point2D

address_for_test_1 = "00:00:00:00:00:01"
address_for_test_2 = "00:00:00:00:00:02"


def test_calculate_average_signal_strength_one_location():
    device = Device(address_for_test_1, [
        frame_factory(0, signal_strength=20),
        frame_factory(0, signal_strength=20),
        frame_factory(0, signal_strength=20),
        frame_factory(0, signal_strength=20),
        frame_factory(0, signal_strength=60),
    ])

    list(calculate_average_signal_strength([device]))
    assert device.averaged_signals[0].variance == 16
    assert device.averaged_signals[0].signal_strength == 28


def test_calculate_average_signal_strength_two_locations():
    device = Device(address_for_test_1, [
        WifiFrame(wlan_radio=WlanRadioInformation(signals=[
            Signal(Point2D(0, 0), 1, 0),
            Signal(Point2D(1, 1), 10, 0),
        ])),
        WifiFrame(wlan_radio=WlanRadioInformation(signals=[
            Signal(Point2D(0, 0), 2, 0),
            Signal(Point2D(1, 1), 20, 0),
        ])),
        WifiFrame(wlan_radio=WlanRadioInformation(signals=[
            Signal(Point2D(0, 0), 3, 0),
            Signal(Point2D(1, 1), 30, 0),
        ])),
        WifiFrame(wlan_radio=WlanRadioInformation(signals=[
            Signal(Point2D(0, 0), 4, 0),
            Signal(Point2D(1, 1), 40, 0),
        ])),
    ])

    list(calculate_average_signal_strength([device]))
    assert device.averaged_signals[0].signal_strength == 2.5
    assert device.averaged_signals[1].signal_strength == 25


def test_calculate_average_signal_strength_multiple_devices():
    devices = [
        Device(address_for_test_1, [
            WifiFrame(wlan_radio=WlanRadioInformation(signals=[
                Signal(Point2D([0, 0]), 1, 0)
            ])),
            WifiFrame(wlan_radio=WlanRadioInformation(signals=[
                Signal(Point2D([0, 0]), 2, 0)
            ])),
            WifiFrame(wlan_radio=WlanRadioInformation(signals=[
                Signal(Point2D([0, 0]), 3, 0)
            ])),
            WifiFrame(wlan_radio=WlanRadioInformation(signals=[
                Signal(Point2D([0, 0]), 4, 0)
            ]))
        ]),
        Device(address_for_test_2, [
            WifiFrame(wlan_radio=WlanRadioInformation(signals=[
                Signal(Point2D([0, 0]), 10, 0)
            ])),
            WifiFrame(wlan_radio=WlanRadioInformation(signals=[
                Signal(Point2D([0, 0]), 20, 0)
            ])),
            WifiFrame(wlan_radio=WlanRadioInformation(signals=[
                Signal(Point2D([0, 0]), 30, 0)
            ])),
            WifiFrame(wlan_radio=WlanRadioInformation(signals=[
                Signal(Point2D([0, 0]), 40, 0)
            ]))
        ]),
    ]

    list(calculate_average_signal_strength(devices))

    assert devices[0].averaged_signals[0].signal_strength == 2.5
    assert devices[1].averaged_signals[0].signal_strength == 25

# def test_it_calculates_rolling_average():
#     # Given 10 wifi frames in a generator, it should produce 10 averages of the signal strength
#     # in a rolling window of 5 frames.
#     wifi_frames = [
#         frame_factory(0, signal_strength=10),
#         frame_factory(0, signal_strength=20),
#         frame_factory(0, signal_strength=30),
#         frame_factory(0, signal_strength=40),
#         frame_factory(0, signal_strength=50),
#         frame_factory(0, signal_strength=60),
#         frame_factory(0, signal_strength=70),
#         frame_factory(0, signal_strength=80),
#         frame_factory(0, signal_strength=90),
#         frame_factory(0, signal_strength=100),
#     ]
#
#     result = calculate_average_signal_strength(wifi_frames, 5)
#
#     # convert to list
#     result = list(result)
#     signal_strengths = [wifi_frame.wlan_radio.signals[0].signal_strength for wifi_frame in result]
#
#     assert signal_strengths == [
#         10, 15, 20, 25, 30, 40, 50, 60, 70, 80
#     ]
#
#
# def test_it_calculates_rolling_variance():
#     # Given 10 wifi frames in a generator, it should produce 10 averages of the signal strength
#     # in a rolling window of 5 frames.
#     wifi_frames = [
#         frame_factory(0, signal_strength=20),
#         frame_factory(0, signal_strength=20),
#         frame_factory(0, signal_strength=20),
#         frame_factory(0, signal_strength=20),
#         frame_factory(0, signal_strength=20),
#         frame_factory(0, signal_strength=60),
#         frame_factory(0, signal_strength=20),
#         frame_factory(0, signal_strength=20),
#         frame_factory(0, signal_strength=20),
#         frame_factory(0, signal_strength=100),
#     ]
#
#     result = calculate_average_signal_strength(wifi_frames, 5)
#
#     # convert to list
#     result = list(result)
#     variances = [wifi_frame.wlan_radio.signals[0].variance for wifi_frame in result]
#
#     assert variances == [
#         0, 0, 0, 0, 0, 16, 16, 16, 16, 32
#     ]
