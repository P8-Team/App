import pandas as pd
from sympy import Point2D

from src.wifi.signal import Signal
from src.wifi.wifi_card import WifiCard
from src.wifi.wlan_radio_information import WlanRadioInformation
from test.utils.wifi_test_utils import Layer

wifi_card = WifiCard("wlan0", Point2D(0, 0))


def test_wlan_radio_information():
    # Arrange
    layer = Layer({
        'wlan_radio.signal_dbm': "-50",
        'wlan_radio.data_rate': "24",
        'wlan_radio.timestamp': "1567757308"
    })

    # Act
    wlan_radio_information = WlanRadioInformation.from_layer(layer, wifi_card, 0)

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
    wlan_radio_information = WlanRadioInformation.from_layer(layer, wifi_card, 0)

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
    wlan_radio_information = WlanRadioInformation.from_layer(layer, wifi_card, 0)

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
    wlan_radio_information1 = WlanRadioInformation.from_layer(layer1, wifi_card, 0)
    wlan_radio_information2 = WlanRadioInformation.from_layer(layer2, wifi_card, 0)

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
    wlan_radio_information1 = WlanRadioInformation.from_layer(layer1, wifi_card, 0)
    wlan_radio_information2 = WlanRadioInformation.from_layer(layer2, wifi_card, 0)

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
    wlan_radio_information1 = WlanRadioInformation.from_layer(layer1, wifi_card, 0)
    wlan_radio_information2 = WlanRadioInformation.from_layer(layer2, wifi_card, 0)

    # Assert
    assert wlan_radio_information1 != wlan_radio_information2


def test_wlan_radio_information_to_dataframe_without_timestamp_delta():
    expected = pd.DataFrame(data=
    {
        'timestamp_delta': [None],
        'data_rate': [12], 'radio_timestamp': [1567757309], 'frequency_mhz': [44]
    })

    wlan_radio_information = WlanRadioInformation(
        [
            Signal(Point2D(1, 1), 1, 1567757309),
            Signal(Point2D(2, 2), 2, 1567757309),
            Signal(Point2D(3, 3), 3, 1567757309)
        ],
        12, 1567757309, 44)

    actual = wlan_radio_information.to_dataframe()

    pd.testing.assert_frame_equal(actual, expected)


def test_wlan_radio_information_to_dataframe_with_timestamp_delta():
    expected = pd.DataFrame(data=
    {
        'timestamp_delta': [10],
        'data_rate': [12], 'radio_timestamp': [1567757309], 'frequency_mhz': [44]
    })

    previous_signal = Signal(Point2D(1, 1), 1, 1567757299)

    signal1 = Signal(Point2D(1, 1), 1, 1567757309)
    signal2 = Signal(Point2D(2, 2), 2, 1567757309)
    signal3 = Signal(Point2D(3, 3), 3, 1567757309)
    signal1.set_timestamp_delta_from_other_signal(previous_signal)
    signal2.set_timestamp_delta_from_other_signal(previous_signal)
    signal3.set_timestamp_delta_from_other_signal(previous_signal)

    wlan_radio_information = WlanRadioInformation(
        [
            signal1,
            signal2,
            signal3
        ],
        12, 1567757309, 44)

    actual = wlan_radio_information.to_dataframe()

    pd.testing.assert_frame_equal(actual, expected)


def test_wlan_radio_information_to_dataframe_uses_lowest_timestamp_delta():
    expected = pd.DataFrame(data=
    {
        'timestamp_delta': [8],
        'data_rate': [12], 'radio_timestamp': [1567757309], 'frequency_mhz': [44]
    })

    previous_signal = Signal(Point2D(1, 1), 1, 1567757299)

    signal1 = Signal(Point2D(1, 1), 1, 1567757307)
    signal2 = Signal(Point2D(2, 2), 2, 1567757308)
    signal3 = Signal(Point2D(3, 3), 3, 1567757309)
    signal1.set_timestamp_delta_from_other_signal(previous_signal)
    signal2.set_timestamp_delta_from_other_signal(previous_signal)
    signal3.set_timestamp_delta_from_other_signal(previous_signal)

    wlan_radio_information = WlanRadioInformation(
        [
            signal1,
            signal2,
            signal3
        ],
        12, 1567757309, 44)

    actual = wlan_radio_information.to_dataframe()

    pd.testing.assert_frame_equal(actual, expected)


def test_wlan_radio_information_smallest_timestamp_delta_returns_none_if_no_deltas():
    signal1 = Signal(Point2D(1, 1), 1, 1567757307)
    signal2 = Signal(Point2D(2, 2), 2, 1567757308)
    signal3 = Signal(Point2D(3, 3), 3, 1567757309)

    wlan_radio_information = WlanRadioInformation(
        [
            signal1,
            signal2,
            signal3
        ],
        12, 1567757309, 44)

    assert wlan_radio_information.get_smallest_timestamp_delta() == None


def test_wlan_radio_information_smallest_timestamp_delta_returns_delta_if_some_deltas_are_not_none():
    previous_signal = Signal(Point2D(1, 1), 1, 1567757299)

    signal1 = Signal(Point2D(1, 1), 1, 1567757307)
    signal2 = Signal(Point2D(2, 2), 2, 1567757308.5)
    signal3 = Signal(Point2D(3, 3), 3, 1567757309)

    signal2.set_timestamp_delta_from_other_signal(previous_signal)

    wlan_radio_information = WlanRadioInformation(
        [
            signal1,
            signal2,
            signal3
        ],
        12, 1567757309, 44)

    assert wlan_radio_information.get_smallest_timestamp_delta() == 9.5


def test_wlan_radio_information_smallest_timestamp_delta_returns_smallest_some_deltas_are_not_none():
    previous_signal = Signal(Point2D(1, 1), 1, 1567757299)

    signal1 = Signal(Point2D(1, 1), 1, 1567757309)
    signal2 = Signal(Point2D(2, 2), 2, 1567757308.5)
    signal3 = Signal(Point2D(3, 3), 3, 1567757307)

    signal1.set_timestamp_delta_from_other_signal(previous_signal)
    signal2.set_timestamp_delta_from_other_signal(previous_signal)
    signal3.set_timestamp_delta_from_other_signal(previous_signal)

    wlan_radio_information = WlanRadioInformation(
        [
            signal1,
            signal2,
            signal3
        ],
        12, 1567757309, 44)

    assert wlan_radio_information.get_smallest_timestamp_delta() == 8
