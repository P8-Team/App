import math
from typing import Iterable

import numpy as np
from scipy.optimize import least_squares, OptimizeResult
import matplotlib.pyplot as plt

from src.distance_strength_calculations import calc_distance_from_dbm_signal_strength
from src.wifi.wifi_frame import WifiFrame


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
        return 1 / (math.pow(self.distance, 4) * math.pow(self.variance, 4))


def non_linear_squared_sum_weighted(x: np.ndarray, anchors: list[Anchor]) -> float:
    return sum(
        [anchor.weight * math.pow((np.linalg.norm(x - anchor.location) - anchor.distance), 2) for anchor in anchors]
    )


def append_location_from_anchors_with_distance(frame: WifiFrame, do_draw=False):
    frequency = frame.wlan_radio.frequency_mhz
    signals = frame.wlan_radio.signals
    # todo where do we get transmission power from?
    transmission_power = 20 if frequency < 4000 else 30  # 20 is max for 2.4ghz, 30 for 5ghz.

    anchors = [Anchor(
        np.array(signal.location.coordinates),
        calc_distance_from_dbm_signal_strength(signal.signal_strength, transmission_power, frequency),
        signal.variance
    ) for signal in signals]

    res = get_least_squared_error(anchors)

    frame.location = res.x.tolist()

    if do_draw:
        draw_plot_with_anchors_circles_and_estimate(anchors, res.x.tolist())

    return frame


def get_least_squared_error(anchors: list[Anchor]) -> OptimizeResult:
    return least_squares(non_linear_squared_sum_weighted, np.array([0, 0]), args=[anchors])


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


def append_location_generator(wifi_frame_generator: Iterable[WifiFrame], do_draw=False) -> Iterable[WifiFrame]:
    for wifi_frame in wifi_frame_generator:
        yield append_location_from_anchors_with_distance(wifi_frame, do_draw)
