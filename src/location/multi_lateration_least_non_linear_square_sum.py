import math

import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

from src.distance_strength_calculations import calc_distance_from_dbm_signal_strength
from src.wifi.wifi_frame import WifiFrame

def non_linear_squared_sum_weighted():
    pass

def non_linear_squared_sum(x, anchors):
    # get sum of squared distances from anchor points
    # to the point x
    return sum([math.pow((np.linalg.norm(x - anchor[0]) - anchor[1]), 2) for anchor in anchors])


def append_location_from_anchors_with_distance(frame: WifiFrame, do_draw=False):
    frequency = frame.wlan_radio.frequency_mhz
    signals = frame.wlan_radio.signals
    anchors = [[np.array(signal["location"]), signal["signal_strength"]] for signal in signals]
    transmission_power = 20 if frequency < 4000 else 30  # 20 is max for 2.4ghz, 30 for 5ghz.
    # [[x,y],distance_dbm]
    # convert to distance in meters
    anchors = [[anchor[0], calc_distance_from_dbm_signal_strength(transmission_power, anchor[1], frequency)] for anchor
               in anchors]

    res = get_least_squared_error(anchors)

    frame.location = res.x.tolist()

    if do_draw:
        draw_plot_with_anchors_circles_and_estimate(anchors, res.x.tolist())

    return frame


def get_least_squared_error(anchors):
    res = least_squares(non_linear_squared_sum, np.array([0, 0]), args=[anchors])
    return res


def draw_plot_with_anchors_circles_and_estimate(anchors, estimate):
    limit_x_max = max([anchor[0][0] + anchor[1] for anchor in anchors])
    limit_x_min = min([anchor[0][0] - anchor[1] for anchor in anchors])
    limit_y_max = max([anchor[0][1] + anchor[1] for anchor in anchors])
    limit_y_min = min([anchor[0][1] - anchor[1] for anchor in anchors])

    fig, ax = plt.subplots()
    ax.set_xlim(limit_x_min, limit_x_max)
    ax.set_ylim(limit_y_min, limit_y_max)
    for anchor in anchors:
        ax.scatter(anchor[0][0], anchor[0][1], s=100, marker='o', color='y')
        ax.add_artist(plt.Circle((anchor[0][0], anchor[0][1]), anchor[1], color='r', fill=False))

    ax.scatter(estimate[0], estimate[1], s=100, marker='o', color='g')

    fig.set_size_inches(10, 10)
    plt.show()
