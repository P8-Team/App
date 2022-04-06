import copy

from src.wifi_frame import WifiFrame
from test.utils.wifi_test_utils import Frame, Layer


def test_construct_wifi_frame():
    # Arrange
    frame = Frame("340", "1647417907.513663000", {
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
    wifi_frame = WifiFrame.from_frame(frame, { 'location': [0, 0] })

    # Assert
    assert wifi_frame.length == 340
    assert wifi_frame.frame_control_information.type == 0
    assert wifi_frame.frame_control_information.subtype == 4
    assert wifi_frame.frame_control_information.receiver_address == '00:0c:29:b7:d9:b0'
    assert wifi_frame.frame_control_information.transmitter_address == '00:0c:29:b7:d9:b1'
    assert len(wifi_frame.wlan_radio.signals) == 1
    assert wifi_frame.wlan_radio.signals[0]["signal_strength"] == -62
    assert wifi_frame.wlan_radio.signals[0]["sniff_timestamp"] == 1647417907.513663000
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
    wifi_frame1 = WifiFrame.from_frame(frame1, { 'location': [0, 0] })
    wifi_frame2 = WifiFrame.from_frame(frame2, { 'location': [0, 0] })

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
    wifi_frame1 = WifiFrame.from_frame(frame1, { 'location': [0, 0] })
    wifi_frame2 = WifiFrame.from_frame(frame2, { 'location': [0, 0] })

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
    wifi_frame1 = WifiFrame.from_frame(frame1, { 'location': [0, 0] })
    wifi_frame2 = WifiFrame.from_frame(frame2, { 'location': [0, 0] })

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
    wifi_frame1 = WifiFrame.from_frame(frame1, { 'location': [0, 0] })
    wifi_frame2 = WifiFrame.from_frame(frame2, { 'location': [0, 0] })

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
    }), { 'location': [0, 0] })
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
    }), { 'location': [0, 0] })
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
    }), { 'location': [0, 0] })
    frame2 = copy.deepcopy(frame1)
    frame2.length = 341

    assert frame1.__key__() != frame2.__key__()
    assert hash(frame1) != hash(frame2)
