from src.wifi_frame import WifiFrame
from utils.wifi_test_utils import Frame, Layer


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
    wifi_frame = WifiFrame(frame)

    # Assert
    assert wifi_frame.length == 340
    assert wifi_frame.sniff_timestamp == 1647417907.513663000
    assert wifi_frame.frame_control_information.type == 0
    assert wifi_frame.frame_control_information.subtype == 4
    assert wifi_frame.frame_control_information.receiver_address == '00:0c:29:b7:d9:b0'
    assert wifi_frame.frame_control_information.transmitter_address == '00:0c:29:b7:d9:b1'
    assert wifi_frame.wlan_radio.rssi == -62
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
    wifi_frame1 = WifiFrame(frame1)
    wifi_frame2 = WifiFrame(frame2)

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
    wifi_frame1 = WifiFrame(frame1)
    wifi_frame2 = WifiFrame(frame2)

    # Assert
    assert wifi_frame1 == wifi_frame2

def test_compare_wifi_frame_different_rssi():
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
    wifi_frame1 = WifiFrame(frame1)
    wifi_frame2 = WifiFrame(frame2)

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
    wifi_frame1 = WifiFrame(frame1)
    wifi_frame2 = WifiFrame(frame2)

    # Assert
    assert wifi_frame1 != wifi_frame2


