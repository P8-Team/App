import pytest
from sympy import Point2D

from src.data_generators.location_data_generator import LocationGenerator
from src.location.distance_strength_calculations import distance_to_signal_strength_free_space_path_loss
from src.location.distance_strength_calculations import mw_to_dbm
from src.wifi.wifi_frame import WifiFrame
from src.wifi.wlan_radio_information import WlanRadioInformation


def __generator_factory_for_test():
    receiver_positions = list()
    receiver_positions.append(Point2D(0, 0))
    receiver_positions.append(Point2D(2, 2))
    receiver_positions.append(Point2D(2, 2))
    return LocationGenerator(receiver_positions)


def test_generator_generates_correct_data_type():
    generator = __generator_factory_for_test()
    element = generator.make_wifi_element(Point2D(5, 0), 20)
    assert isinstance(element, WifiFrame)


def test_generator_raises_typeerror_on_incorrect_positions_input():
    positions = list()
    positions.append("Not A Point")
    with pytest.raises(TypeError):
        LocationGenerator(positions)


def test_generator_generates_correct_data_types_contains_wlan_radio_information_object():
    generator = __generator_factory_for_test()
    element = generator.make_wifi_element(Point2D(1, 1), 20)
    assert hasattr(element, 'wlan_radio')
    assert isinstance(element.wlan_radio, WlanRadioInformation)


def test_generator_generates_correct_data_with_correct_dbm_output():
    element = distance_to_signal_strength_free_space_path_loss(0.007957747154594767, 3000, 100)
    assert element == pytest.approx(100)


def test_mw_to_dmb():
    assert mw_to_dbm(100) == 20
    assert mw_to_dbm(1) == 0
    assert mw_to_dbm(0.01) == pytest.approx(-20)
    assert mw_to_dbm(0.00001) == -50
    assert mw_to_dbm(100000) == pytest.approx(50)
