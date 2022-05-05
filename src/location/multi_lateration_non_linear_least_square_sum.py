import math
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from scipy.optimize import least_squares, OptimizeResult

from src.device.device import Device
from src.location.distance_strength_calculations import calc_distance_from_dbm_signal_strength


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

    if device.identification is not None:
        transmission_power_dbm = device.identification["transmission_power_dbm"]
    else:
        # 20 is max for 2.4ghz, 30 for 5ghz.
        transmission_power_dbm = 20 if frequency < 4000 else 30

    anchors = [Anchor(
        np.array(signal.location.coordinates, dtype=np.float64),
        calc_distance_from_dbm_signal_strength(transmission_power_dbm, signal.signal_strength, frequency),
        signal.variance
    ) for signal in signals]

    res = get_least_squared_error(anchors)

    device.position = res.x.tolist()

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    X = np.arange(-4, 8, 0.1)
    Y = np.arange(-4, 8, 0.1)
    X, Y = np.meshgrid(X, Y)

    Z = np.zeros(X.shape)


    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = non_linear_squared_sum_weighted(np.array([X[i, j], Y[i, j]]), anchors)

    ax.plot_surface(X, Y, Z, rstride=5, cstride=5, cmap=cm.hsv,
                    linewidth=50, antialiased=True)
    # ax.invert_zaxis()
    plt.show()

    plt.style.use('_mpl-gallery-nogrid')
    fig, ax = plt.subplots()
    ax.set_title('Least Squared Error')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.imshow(Z, cmap=plt.cm.gist_rainbow, interpolation='nearest')
    plt.show()

    levels = np.geomspace(Z.min(), Z.max(), 10)
    # levels = np.linspace(Z.min(), 0.01, 8)
    # levels = np.logspace(0, Z.max(), 256)

    # plot
    fig, ax = plt.subplots()

    ax.contourf(X, Y, Z, levels=levels)

    plt.show()

    fig, axs = plt.subplots(1, 2, figsize=(6, 3), sharey=True)
    axs[0].set_xlim(-4,8)
    axs[0].set_ylim(-4,8)
    for anchor in anchors:
        axs[0].scatter(anchor.location[0], anchor.location[1], s=100, marker='o', color='y')
        axs[0].add_artist(plt.Circle((anchor.location[0], anchor.location[1]), anchor.distance, color='r', fill=False))

    axs[0].scatter(device.position[0], device.position[1], s=100, marker='o', color='g')

    axs[1].set_xlim(-4,8)
    axs[1].set_ylim(-4,8)
    for anchor in anchors:
        axs[1].scatter(anchor.location[0], anchor.location[1], s=100, marker='o', color='y')
        axs[1].add_artist(plt.Circle((anchor.location[0], anchor.location[1]), anchor.distance, color='r', fill=False))

    axs[1].scatter(device.position[0], device.position[1], s=100, marker='o', color='g')

    # fig.set_size_inches(10, 10)
    plt.show()


    if do_draw:
        draw_plot_with_anchors_circles_and_estimate(anchors, device.position)


def get_least_squared_error(anchors: list[Anchor]) -> OptimizeResult:
    return least_squares(non_linear_squared_sum_weighted, np.array([0, 0]), args=[anchors], gtol=None, verbose=2)


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
    ax.set_xlim(-4,8)
    ax.set_ylim(-4,8)
    for anchor in anchors:
        ax.scatter(anchor.location[0], anchor.location[1], s=100, marker='o', color='y')
        ax.add_artist(plt.Circle((anchor.location[0], anchor.location[1]), anchor.distance, color='r', fill=False))

    ax.scatter(estimate[0], estimate[1], s=100, marker='o', color='g')

    fig.set_size_inches(10, 10)
    plt.show()


def append_location_generator(generator: Iterable[Device], do_draw=False) -> Iterable[Device]:
    for device in generator:
        calculate_position(device, do_draw)
        yield device
