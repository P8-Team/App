import math

import pytest

from src.location.distance_strength_calculations import dbm_to_mw, \
    calc_distance_from_mw_signal_strength_free_space_path_loss, \
    signal_strength_dbm_to_distance, calc_distance_from_dbm_signal_strength_free_space_path_loss, \
    distance_to_signal_strength


def test_mw_from_dbm():
    assert dbm_to_mw(20) == 100
    assert dbm_to_mw(0) == 1
    assert dbm_to_mw(-20) == 0.01
    assert dbm_to_mw(-50) == 0.00001
    assert dbm_to_mw(50) == 100000


def test_calc_distance_from_mw_signal_strength_free_space_path_loss_():
    assert calc_distance_from_mw_signal_strength_free_space_path_loss(100, 100, 3000) == pytest.approx(
        1 / (40 * math.pi))  # 7 cm
    assert calc_distance_from_mw_signal_strength_free_space_path_loss(0.1, 0.001, 3000) == pytest.approx(
        0.001 / (0.004 * math.pi))  # 8 cm
    assert calc_distance_from_mw_signal_strength_free_space_path_loss(0.1, 0.0001, 2400) == pytest.approx(
        0.314557575653044)  # 31 cm


def test_calc_distance_free_space_path_loss_from_mw_signal_strength_real_data():
    # possible real data
    # 1000mW transmission, -30dbM signal, 5800MHz frequency
    assert calc_distance_from_mw_signal_strength_free_space_path_loss(1000, 0.001, 5800) == pytest.approx(4.1160761)
    # 1000mW tranmission, -50dBm signal, 5800Mhz frequency
    assert calc_distance_from_mw_signal_strength_free_space_path_loss(1000, 0.00001, 5800) == pytest.approx(41.16076114)
    # 1000mW tranmission, -60dBm signal, 5800Mhz frequency
    assert calc_distance_from_mw_signal_strength_free_space_path_loss(1000, 0.0000001, 5800) == pytest.approx(
        411.6076114)
    # 1000mW tranmission, -70dBm signal, 5800Mhz frequency
    assert calc_distance_from_mw_signal_strength_free_space_path_loss(1000, 0.00000001, 5800) == pytest.approx(
        1301.6175544)
    # 1000mW tranmission, -80dBm signal, 5800Mhz frequency
    assert calc_distance_from_mw_signal_strength_free_space_path_loss(1000, 0.000000001, 5800) == pytest.approx(
        4116.0761144)


def test_calc_distance_from_dbm_signal_strength_real_data():
    # possible real data
    assert signal_strength_dbm_to_distance(10, -30, 4) == pytest.approx(10)
    assert signal_strength_dbm_to_distance(10, -50, 4) == pytest.approx(31.622776601683793)
    assert signal_strength_dbm_to_distance(10, -70, 4) == pytest.approx(100)
    assert signal_strength_dbm_to_distance(20, -30, 2) == pytest.approx(316.22776601683796)
    assert signal_strength_dbm_to_distance(0, -30, 4) == pytest.approx(5.6234132561903491)


def test_calc_received_power_from_transmitted_power_and_path_loss_exponent():
    assert distance_to_signal_strength(10, 10, 4) == -30
    assert distance_to_signal_strength(100, 10, 4) == -70


def test_calc_distance_from_dbm_signal_strength():
    assert calc_distance_from_dbm_signal_strength_free_space_path_loss(30, -50, 5800) == pytest.approx(41.16076114)


def test_calc_distance_from_mw_signal_strength_with_zero_r_fails():
    with pytest.raises(ZeroDivisionError):
        calc_distance_from_mw_signal_strength_free_space_path_loss(100, 0, 3000)


def test_calc_distance_from_mw_signal_strength_with_zero_frequency_fails():
    with pytest.raises(ZeroDivisionError):
        calc_distance_from_mw_signal_strength_free_space_path_loss(100, 100, 0)


def test_calc_distance_from_mw_signal_strength_with_negative_frequency_fails():
    # Assert ValueError with negative frequency
    with pytest.raises(ValueError):
        calc_distance_from_mw_signal_strength_free_space_path_loss(100, 100, -3000)


def test_calc_distance_from_mw_signal_strength_with_negative_t_fails():
    with pytest.raises(ValueError):
        calc_distance_from_mw_signal_strength_free_space_path_loss(-100, 100, 3000)


def test_calc_distance_from_mw_signal_strength_with_negative_r_fails():
    with pytest.raises(ValueError):
        calc_distance_from_mw_signal_strength_free_space_path_loss(100, -100, 3000)
