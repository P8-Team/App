import math


def calc_distance_from_mw_signal_strength(tp, rp, freq_in_mhz):
    if freq_in_mhz < 0:
        raise ValueError("frequency must be positive")

    # calculate wavelength with speed of light and frequency
    l = 300/freq_in_mhz # 0.1 * 10 * 10 * 4*100*pi
    # Formula from http://www.sis.pitt.edu/prashk/inf1072/Fall16/lec5.pdf
    d = (l * math.sqrt(rp) * math.sqrt(tp))/(4*math.pi*rp)
    return d


def dbm_to_mw(dbm):
    return math.pow(10,dbm/10)


def calc_distance_from_dbm_signal_strength(tp, rp, freq_in_mhz):
    return calc_distance_from_mw_signal_strength(dbm_to_mw(tp), dbm_to_mw(rp), freq_in_mhz)