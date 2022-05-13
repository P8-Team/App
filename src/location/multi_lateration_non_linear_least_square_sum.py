import math
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares, OptimizeResult

from src.device.device import Device
from src.location.distance_strength_calculations import signal_strength_dbm_to_distance


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

        if math.isclose(self.distance, 0, abs_tol=1e-8) or math.isclose(self.variance, 0, abs_tol=1e-10):
            return 1
        return 1 / (math.pow(self.distance, 4) * math.pow(self.variance, 4))


def non_linear_squared_sum_weighted(x: np.ndarray, anchors: list[Anchor]) -> float:
    return sum(
        [anchor.weight * math.pow((np.linalg.norm(x - anchor.location) - anchor.distance), 2) for anchor in anchors]
    )


def calculate_position(device: Device, path_loss_exponent, do_draw=False):
    frequency = device.frames[-1].wlan_radio.frequency_mhz
    signals = device.averaged_signals

    if device.identification is not None:
        transmission_power_dbm = int(device.identification[0])
    else:
        # 20 is max for 2.4ghz, 30 for 5ghz.
        transmission_power_dbm = 20 if frequency < 4000 else 30

    anchors = [Anchor(
        np.array(signal.location.coordinates, dtype=np.float64),
        signal_strength_dbm_to_distance(transmission_power_dbm, signal.signal_strength, path_loss_exponent),
        signal.variance
    ) for signal in signals]

    res = get_least_squared_error(anchors)

    device.position = res.x.tolist()

    if do_draw:
        draw_plot_with_anchors_circles_and_estimate(anchors, device.position)


def get_least_squared_error(anchors: list[Anchor]) -> OptimizeResult:
    return least_squares(non_linear_squared_sum_weighted, np.array([0, 0]), args=[anchors], gtol=None)



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


def append_location_generator(generator: Iterable[Device], path_loss_exponent, do_draw=False) -> Iterable[Device]:
    for device in generator:
        calculate_position(device, path_loss_exponent, do_draw)
        yield device
