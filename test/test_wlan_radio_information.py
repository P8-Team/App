from src.wlan_radio_information import WlanRadioInformation
from test.utils.wifi_test_utils import Layer
import pandas as pd


def test_wlan_radio_information():
    # Arrange
    layer = Layer({
        'wlan_radio.signal_dbm': "-50",
        'wlan_radio.data_rate': "24",
        'wlan_radio.timestamp': "1567757308"
    })

    # Act
    wlan_radio_information = WlanRadioInformation.from_layer(layer, { 'location': [0, 0] }, 0)

    # Assert
    assert wlan_radio_information.data_rate == 24
    assert wlan_radio_information.radio_timestamp == 1567757308


def test_wlan_radio_information_construct_missing_information():
    # Arrange
    layer = Layer({
        'wlan_radio.signal_dbm': "-50",
        'wlan_radio.timestamp': "1567757308"
    })

    # Act
    wlan_radio_information = WlanRadioInformation.from_layer(layer, { 'location': [0, 0] }, 0)

    # Assert
    assert wlan_radio_information.data_rate is None
    assert wlan_radio_information.radio_timestamp == 1567757308


def test_wlan_radio_information_construct_with_float():
    # Arrange
    layer = Layer({
        'wlan_radio.signal_dbm': "-50.5",
        'wlan_radio.data_rate': "24.2",
    })

    # Act
    wlan_radio_information = WlanRadioInformation.from_layer(layer, { 'location': [0, 0] }, 0)

    # Assert
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
    wlan_radio_information1 = WlanRadioInformation.from_layer(layer1, { 'location': [0, 0] }, 0)
    wlan_radio_information2 = WlanRadioInformation.from_layer(layer2, { 'location': [0, 0] }, 0)

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
    wlan_radio_information1 = WlanRadioInformation.from_layer(layer1, { 'location': [0, 0] }, 0)
    wlan_radio_information2 = WlanRadioInformation.from_layer(layer2, { 'location': [0, 0] }, 0)

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
    wlan_radio_information1 = WlanRadioInformation.from_layer(layer1, { 'location': [0, 0] }, 0)
    wlan_radio_information2 = WlanRadioInformation.from_layer(layer2, { 'location': [0, 0] }, 0)

    # Assert
    assert wlan_radio_information1 != wlan_radio_information2

def test_wlan_radio_information_to_dataframe():
    expected = pd.DataFrame(data = 
        {
         'signal_strength': [1], 'location': [[1,1]], 'sniff_timestamp': [1567757309],
         'signal_strength_1': [2], 'location_1': [[2,2]], 'sniff_timestamp_1': [1567757309],
         'signal_strength_2': [3], 'location_2': [[3,3]], 'sniff_timestamp_2': [1567757309],
         'data_rate': [12], 'radio_timestamp': [1567757309], 'frequency_mhz': [44]
        })

    wlan_radio_information = WlanRadioInformation(
        [
            {'signal_strength': 1, 'location': [1,1], 'sniff_timestamp': 1567757309}, 
            {'signal_strength': 2, 'location': [2,2], 'sniff_timestamp': 1567757309}, 
            {'signal_strength': 3, 'location': [3,3], 'sniff_timestamp': 1567757309}
        ],
        12, 1567757309, 44)

    actual = wlan_radio_information.to_dataframe()

    pd.testing.assert_frame_equal(actual, expected)