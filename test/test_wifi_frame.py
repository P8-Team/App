import copy
import uuid

import pandas as pd
from sympy import Point2D

from src.wifi.frame_control_information import FrameControlInformation
from src.wifi.signal import Signal
from src.wifi.wifi_card import WifiCard
from src.wifi.wifi_frame import WifiFrame
from src.wifi.wlan_radio_information import WlanRadioInformation
from test.utils.wifi_test_utils import Frame, Layer


def test_construct_wifi_frame():
    # Arrange
    frame = Frame("340", "1647417907.513663000", {
        'wlan': Layer({
            'fcs': '0x1234',
            'wlan.fc.type': '0',
            'wlan.fc.subtype': '4',
            'wlan.ra_resolved': '00:0c:29:b7:d9:b0',
            'wlan.ta_resolved': '00:0c:29:b7:d9:b1',
        }),
        'wlan_radio': Layer({
            'wlan_radio.signal_dbm': '-62',
            'wlan_radio.data_rate': '54',
            'wlan_radio.timestamp': '1567757308'
        })
    })

    # Act
    wifi_frame = WifiFrame.from_frame(frame, WifiCard("wlan0", Point2D(0, 0)))

    # Assert
    assert wifi_frame.length == 340
    assert wifi_frame.frame_control_sequence == 4660
    assert wifi_frame.frame_control_information.type == 0
    assert wifi_frame.frame_control_information.subtype == 4
    assert wifi_frame.frame_control_information.receiver_address == '00:0c:29:b7:d9:b0'
    assert wifi_frame.frame_control_information.transmitter_address == '00:0c:29:b7:d9:b1'
    assert len(wifi_frame.wlan_radio.signals) == 1
    assert wifi_frame.wlan_radio.signals[0].signal_strength == -62
    assert wifi_frame.wlan_radio.signals[0].sniff_timestamp == 1647417907.513663000
    assert wifi_frame.wlan_radio.data_rate == 54
    assert wifi_frame.wlan_radio.radio_timestamp == 1567757308


def test_compare_wifi_frame_identical():
    # Arrange
    frame1 = Frame("340", "1647417907.513663000", {
        'wlan': Layer({
            'wlan.fc.type': '0',
            'wlan.fc.subtype': '4',
            'wlan.ra_resolved': '00:0c:29:b7:d9:b0',
            'wlan.ta_resolved': '00:0c:29:b7:d9:b1',
        }),
        'wlan_radio': Layer({
            'wlan_radio.signal_dbm': '-62',
            'wlan_radio.data_rate': '54',
            'wlan_radio.timestamp': '1567757308'
        })
    })
    frame2 = Frame("340", "1647417907.513663000", {
        'wlan': Layer({
            'wlan.fc.type': '0',
            'wlan.fc.subtype': '4',
            'wlan.ra_resolved': '00:0c:29:b7:d9:b0',
            'wlan.ta_resolved': '00:0c:29:b7:d9:b1',
        }),
        'wlan_radio': Layer({
            'wlan_radio.signal_dbm': '-62',
            'wlan_radio.data_rate': '54',
            'wlan_radio.timestamp': '1567757308'
        })
    })

    # Act
    wifi_frame1 = WifiFrame.from_frame(frame1, WifiCard("wlan0", Point2D(0, 0)))
    wifi_frame2 = WifiFrame.from_frame(frame2, WifiCard("wlan0", Point2D(0, 0)))

    # Assert
    assert wifi_frame1 == wifi_frame2


def test_compare_wifi_frame_different_timestamp():
    # Arrange
    frame1 = Frame("340", "1647417907.513663000", {
        'wlan': Layer({
            'wlan.fc.type': '0',
            'wlan.fc.subtype': '4',
            'wlan.ra_resolved': '00:0c:29:b7:d9:b0',
            'wlan.ta_resolved': '00:0c:29:b7:d9:b1',
        }),
        'wlan_radio': Layer({
            'wlan_radio.signal_dbm': '-62',
            'wlan_radio.data_rate': '54',
            'wlan_radio.timestamp': '1567757308'
        })
    })
    frame2 = Frame("340", "1647417900.513663000", {
        'wlan': Layer({
            'wlan.fc.type': '0',
            'wlan.fc.subtype': '4',
            'wlan.ra_resolved': '00:0c:29:b7:d9:b0',
            'wlan.ta_resolved': '00:0c:29:b7:d9:b1',
        }),
        'wlan_radio': Layer({
            'wlan_radio.signal_dbm': '-62',
            'wlan_radio.data_rate': '54',
            'wlan_radio.timestamp': '1567757308'
        })
    })

    # Act
    wifi_frame1 = WifiFrame.from_frame(frame1, WifiCard("wlan0", Point2D(0, 0)))
    wifi_frame2 = WifiFrame.from_frame(frame2, WifiCard("wlan0", Point2D(0, 0)))

    # Assert
    assert wifi_frame1 == wifi_frame2


def test_compare_wifi_frame_different_signal_strength():
    # Arrange
    frame1 = Frame("340", "1647417907.513663000", {
        'wlan': Layer({
            'wlan.fc.type': '0',
            'wlan.fc.subtype': '4',
            'wlan.ra_resolved': '00:0c:29:b7:d9:b0',
            'wlan.ta_resolved': '00:0c:29:b7:d9:b1',
        }),
        'wlan_radio': Layer({
            'wlan_radio.signal_dbm': '-62',
            'wlan_radio.data_rate': '54',
            'wlan_radio.timestamp': '1567757308'
        })
    })
    frame2 = Frame("340", "1647417907.513663000", {
        'wlan': Layer({
            'wlan.fc.type': '0',
            'wlan.fc.subtype': '4',
            'wlan.ra_resolved': '00:0c:29:b7:d9:b0',
            'wlan.ta_resolved': '00:0c:29:b7:d9:b1',
        }),
        'wlan_radio': Layer({
            'wlan_radio.signal_dbm': '-63',
            'wlan_radio.data_rate': '54',
            'wlan_radio.timestamp': '1567757308'
        })
    })

    # Act
    wifi_frame1 = WifiFrame.from_frame(frame1, WifiCard("wlan0", Point2D(0, 0)))
    wifi_frame2 = WifiFrame.from_frame(frame2, WifiCard("wlan0", Point2D(0, 0)))

    # Assert
    assert wifi_frame1 == wifi_frame2


def test_compare_wifi_frame_different():
    # Arrange
    frame1 = Frame("340", "1647417907.513663000", {
        'wlan': Layer({
            'wlan.fc.type': '0',
            'wlan.fc.subtype': '4',
            'wlan.ra_resolved': '00:0c:29:b7:d9:b0',
            'wlan.ta_resolved': '00:0c:29:b7:d9:b1',
        }),
        'wlan_radio': Layer({
            'wlan_radio.signal_dbm': '-62',
            'wlan_radio.data_rate': '54',
            'wlan_radio.timestamp': '1567757308'
        })
    })
    frame2 = Frame("341", "1647417905.513663000", {
        'wlan': Layer({
            'wlan.fc.type': '1',
            'wlan.fc.subtype': '5',
            'wlan.ra_resolved': '00:0c:29:b7:d9:b1',
            'wlan.ta_resolved': '00:0c:29:b7:d9:b2',
        }),
        'wlan_radio': Layer({
            'wlan_radio.signal_dbm': '-64',
            'wlan_radio.data_rate': '55',
            'wlan_radio.timestamp': '1567757309'
        })
    })

    # Act
    wifi_frame1 = WifiFrame.from_frame(frame1, WifiCard("wlan0", Point2D(0, 0)))
    wifi_frame2 = WifiFrame.from_frame(frame2, WifiCard("wlan0", Point2D(0, 0)))

    # Assert
    assert wifi_frame1 != wifi_frame2


def test_wifi_frame_has_same_hash_with_different_rrsi_and_sniff_timestamp():
    frame1 = WifiFrame.from_frame(Frame("340", "1647417907.513663000", {
        'wlan': Layer({
            'wlan.fc.type': '0',
            'wlan.fc.subtype': '4',
            'wlan.ra_resolved': '00:0c:29:b7:d9:b0',
            'wlan.ta_resolved': '00:0c:29:b7:d9:b1',
        }),
        'wlan_radio': Layer({
            'wlan_radio.signal_dbm': '-62',
            'wlan_radio.data_rate': '54',
            'wlan_radio.timestamp': '1567757308'
        })
    }), WifiCard("wlan0", Point2D(0, 0)))
    # Copy frame 1 and change the signal_strength and sniff timestamp

    frame2 = copy.deepcopy(frame1)
    frame2.sniff_timestamp = 1647417905.513663000
    frame2.wlan_radio.signal_strength = -63

    assert frame1.__key__() == frame2.__key__()
    assert hash(frame1) == hash(frame2)


def test_wifi_frame_has_same_hash_identical():
    frame1 = WifiFrame.from_frame(Frame("340", "1647417907.513663000", {
        'wlan': Layer({
            'wlan.fc.type': '0',
            'wlan.fc.subtype': '4',
            'wlan.ra_resolved': '00:0c:29:b7:d9:b0',
            'wlan.ta_resolved': '00:0c:29:b7:d9:b1',
        }),
        'wlan_radio': Layer({
            'wlan_radio.signal_dbm': '-62',
            'wlan_radio.data_rate': '54',
            'wlan_radio.timestamp': '1567757308'
        })
    }), WifiCard("wlan0", Point2D(0, 0)))
    frame2 = copy.deepcopy(frame1)

    assert frame1.__key__() == frame2.__key__()
    assert hash(frame1) == hash(frame2)


def test_wifi_frame_has_different_hash():
    frame1 = WifiFrame.from_frame(Frame("340", "1647417907.513663000", {
        'wlan': Layer({
            'wlan.fc.type': '0',
            'wlan.fc.subtype': '4',
            'wlan.ra_resolved': '00:0c:29:b7:d9:b0',
            'wlan.ta_resolved': '00:0c:29:b7:d9:b1',
        }),
        'wlan_radio': Layer({
            'wlan_radio.signal_dbm': '-62',
            'wlan_radio.data_rate': '54',
            'wlan_radio.timestamp': '1567757308'
        })
    }), WifiCard("wlan0", Point2D(0, 0)))
    frame2 = copy.deepcopy(frame1)
    frame2.length = 341

    assert frame1.__key__() != frame2.__key__()
    assert hash(frame1) != hash(frame2)


def test_wifi_frame_to_dataframe():
    expected = pd.DataFrame(data=
    {
        'length': 12,
        'signal_strength_0': [1], 'timestamp_delta_0': [None],
        'signal_strength_1': [2], 'timestamp_delta_1': [None],
        'signal_strength_2': [3], 'timestamp_delta_2': [None],
        'data_rate': [12], 'radio_timestamp': [1567757309], 'frequency_mhz': [44],
        'type': [0],
        'subtype': [10],
        'receiver_address': ['b4:de:31:9c:f0:8a'],
        'transmitter_address': ['50:e0:85:3f:77:5e']
    })

    frame_control_information = FrameControlInformation(0, 10, 'b4:de:31:9c:f0:8a', '50:e0:85:3f:77:5e')
    wlan_radio_information = WlanRadioInformation(
        [
            Signal(Point2D(1, 1), 1, 1567757309),
            Signal(Point2D(2, 2), 2, 1567757309),
            Signal(Point2D(3, 3), 3, 1567757309)
        ],
        12, 1567757309, 44)

    wifi_frame = WifiFrame(12, uuid.uuid4().int, wlan_radio_information, frame_control_information)

    actual = wifi_frame.to_dataframe()

    pd.testing.assert_frame_equal(actual, expected)
