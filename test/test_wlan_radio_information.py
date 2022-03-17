from src.wlan_radio_information import WlanRadioInformation
from test.utils.wifi_test_utils import Layer


def test_wlan_radio_information():
    # Arrange
    layer = Layer({
        'wlan_radio.signal_dbm': "-50",
        'wlan_radio.data_rate': "24",
        'wlan_radio.timestamp': "1567757308"
    })

    # Act
    wlan_radio_information = WlanRadioInformation.from_layer(layer)

    # Assert
    assert wlan_radio_information.rssi == -50
    assert wlan_radio_information.data_rate == 24
    assert wlan_radio_information.radio_timestamp == 1567757308


def test_wlan_radio_information_construct_missing_information():
    # Arrange
    layer = Layer({
        'wlan_radio.signal_dbm': "-50",
        'wlan_radio.timestamp': "1567757308"
    })

    # Act
    wlan_radio_information = WlanRadioInformation.from_layer(layer)

    # Assert
    assert wlan_radio_information.rssi == -50
    assert wlan_radio_information.data_rate is None
    assert wlan_radio_information.radio_timestamp == 1567757308


def test_wlan_radio_information_construct_with_float():
    # Arrange
    layer = Layer({
        'wlan_radio.signal_dbm': "-50.5",
        'wlan_radio.data_rate': "24.2",
    })

    # Act
    wlan_radio_information = WlanRadioInformation.from_layer(layer)

    # Assert
    assert wlan_radio_information.rssi == -50.5
    assert wlan_radio_information.data_rate == 24.2


def test_compare_wlan_radio_information_identical():
    # Arrange
    layer1 = Layer({
        'wlan_radio.signal_dbm': "-50",
        'wlan_radio.data_rate': "24",
        'wlan_radio.timestamp': "1567757308"
    })

    layer2 = Layer({
        'wlan_radio.signal_dbm': "-50",
        'wlan_radio.data_rate': "24",
        'wlan_radio.timestamp': "1567757308"
    })

    # Act
    wlan_radio_information1 = WlanRadioInformation.from_layer(layer1)
    wlan_radio_information2 = WlanRadioInformation.from_layer(layer2)

    # Assert
    assert wlan_radio_information1 == wlan_radio_information2


def test_compare_wlan_radio_information_different_rrsi():
    # Arrange
    layer1 = Layer({
        'wlan_radio.signal_dbm': "-50",
        'wlan_radio.data_rate': "24",
        'wlan_radio.timestamp': "1567757308"
    })

    layer2 = Layer({
        'wlan_radio.signal_dbm': "-60",
        'wlan_radio.data_rate': "24",
        'wlan_radio.timestamp': "1567757308"
    })

    # Act
    wlan_radio_information1 = WlanRadioInformation.from_layer(layer1)
    wlan_radio_information2 = WlanRadioInformation.from_layer(layer2)

    # Assert
    assert wlan_radio_information1 == wlan_radio_information2


def test_compare_wlan_radio_information_different():
    # Arrange
    layer1 = Layer({
        'wlan_radio.signal_dbm': "-50",
        'wlan_radio.data_rate': "24",
        'wlan_radio.timestamp': "1567757308"
    })

    layer2 = Layer({
        'wlan_radio.signal_dbm': "-50",
        'wlan_radio.data_rate': "24",
        'wlan_radio.timestamp': "1567757309"
    })

    # Act
    wlan_radio_information1 = WlanRadioInformation.from_layer(layer1)
    wlan_radio_information2 = WlanRadioInformation.from_layer(layer2)

    # Assert
    assert wlan_radio_information1 != wlan_radio_information2
