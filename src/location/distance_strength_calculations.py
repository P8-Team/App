import math


def calc_distance_from_mw_signal_strength_free_space_path_loss(tp, rp, freq_in_mhz):
    if freq_in_mhz < 0:
        raise ValueError("frequency must be positive")

    # calculate wavelength with speed of light and frequency
    l = wavelength(freq_in_mhz)
    # Formula from http://www.sis.pitt.edu/prashk/inf1072/Fall16/lec5.pdf
    d = (l * math.sqrt(rp) * math.sqrt(tp)) / (4 * math.pi * rp)
    return d


def dbm_to_mw(dbm):
    return math.pow(10, dbm / 10)


def mw_to_dbm(mw):
    return 10 * math.log(mw, 10)


def signal_strength_dbm_to_distance(tp, rp, path_loss_exponent):
    return math.pow(10, (tp - rp) / (10 * path_loss_exponent))


def calc_distance_from_dbm_signal_strength_free_space_path_loss(tp, rp, freq_in_mhz):
    return calc_distance_from_mw_signal_strength_free_space_path_loss(dbm_to_mw(tp), dbm_to_mw(rp), freq_in_mhz)


def wavelength(frequency):
    """
    Wavelength calculation
    :param frequency: Frequency in mhz
    :return:
    """
    return 300 / frequency


def distance_to_signal_strength(distance, transmission_power, path_loss_exponent):
    return -10 * path_loss_exponent * math.log(distance, 10) + transmission_power


def distance_to_signal_strength_free_space_path_loss(distance, frequency, transmission_power):
    if distance <= 0:
        raise TypeError("Distance should be more than 0")
    wl = wavelength(frequency)

    return (transmission_power * pow(wl, 2)) / pow(4 * math.pi * distance, 2)
