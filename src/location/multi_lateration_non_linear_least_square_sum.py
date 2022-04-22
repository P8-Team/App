import math
from typing import Iterable

import numpy as np
from scipy.optimize import least_squares, OptimizeResult
import matplotlib.pyplot as plt

from src.location.distance_strength_calculations import calc_distance_from_dbm_signal_strength
from src.wifi.wifi_frame import WifiFrame
from src.device.device import Device


class Anchor:
    location: np.ndarray
    distance: float
    variance: float
    weight: float

    def __init__(self, location: np.ndarray, distance: float, variance: float):
        self.location = location
        self.distance = distance
        assert variance is not None
        self.variance = variance
        self.weight = self.calc_weight()

    def calc_weight(self) -> float:
        # The article does not mention this edge case. It is assumed that the weight is 1.
        if self.distance == 0 or self.variance == 0:
            return 1
        return 1 / (math.pow(self.distance, 4) * math.pow(self.variance, 4))


def non_linear_squared_sum_weighted(x: np.ndarray, anchors: list[Anchor]) -> float:
    return sum(
        [anchor.weight * math.pow((np.linalg.norm(x - anchor.location) - anchor.distance), 2) for anchor in anchors]
    )


def calculate_position(device: Device, do_draw=False):
    frequency = device.frames[-1].wlan_radio.frequency_mhz
    signals = device.averaged_signals

    # 20 is max for 2.4ghz, 30 for 5ghz.
    transmission_power = device.identification["transmission_power"] if device.identification is not None \
        else (20 if frequency < 4000 else 30)

    anchors = [Anchor(
        np.array(signal.location.coordinates, dtype=np.float64),
        calc_distance_from_dbm_signal_strength(transmission_power, signal.signal_strength, frequency),
        signal.variance
    ) for signal in signals]

    res = get_least_squared_error(anchors)

    device.position = res.x.tolist()

    if do_draw:
        draw_plot_with_anchors_circles_and_estimate(anchors, res.x.tolist())


def get_least_squared_error(anchors: list[Anchor]) -> OptimizeResult:
    return least_squares(non_linear_squared_sum_weighted, np.array([0, 0]), args=[anchors])


def draw_plot_with_anchors_circles_and_estimate(anchors, estimate):
    """
        Can be used to draw a plot with the anchors, their radius circles and the estimate.
    """
    # Limit plot size to the anchors circles and the estimate.
    limit_x_max = max([anchor.location[0] + anchor.distance for anchor in anchors])
    limit_x_min = min([anchor.location[0] - anchor.distance for anchor in anchors])
    limit_y_max = max([anchor.location[1] + anchor.distance for anchor in anchors])
    limit_y_min = min([anchor.location[1] - anchor.distance for anchor in anchors])

    fig, ax = plt.subplots()
    ax.set_xlim(limit_x_min, limit_x_max)
    ax.set_ylim(limit_y_min, limit_y_max)
    for anchor in anchors:
        ax.scatter(anchor.location[0], anchor.location[1], s=100, marker='o', color='y')
        ax.add_artist(plt.Circle((anchor.location[0], anchor.location[1]), anchor.distance, color='r', fill=False))

    ax.scatter(estimate[0], estimate[1], s=100, marker='o', color='g')

    fig.set_size_inches(10, 10)
    plt.show()


def append_location_generator(wifi_frame_generator: Iterable[WifiFrame], do_draw=False) -> Iterable[WifiFrame]:
    for wifi_frame in wifi_frame_generator:
        yield calculate_position(wifi_frame, do_draw)
