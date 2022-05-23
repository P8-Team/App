from os import listdir
from os.path import isfile, join

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from figures.evaluation import euclidean_distance, get_weighted


def make_scatter_plot(axs, path, expected_location, limits, title):
    print("Path: " + path)
    data = pd.read_csv(join("results", path), sep=',')

    x = data['x'].to_list()
    y = data['y'].to_list()
    axs.scatter(expected_location[0], expected_location[1], c='black', marker='x')
    axs.scatter(x, y, s=1)
    # add legend
    axs.legend(['Actual location', 'Estimated locations'], loc='upper right')
    axs.set_xlabel('x (m)')
    axs.set_ylabel('y (m)')
    # make the axis max and min 20% bigger
    axs.set_xlim(limits[0], limits[1])
    axs.set_ylim(limits[2], limits[3])
    axs.grid(True)
    axs.set_title(title)


def make_error_plot(axs, path, expected_location, ylimits, title):
    print("Path: " + path)
    data = pd.read_csv(join("results", path), sep=',')
    x = data['x'].to_list()
    y = data['y'].to_list()
    error = euclidean_distance(x, y, expected_location)

    axs.set_xlabel('measurement #')
    axs.set_ylabel(f'error (euclidean distance in meters to {expected_location})')
    axs.set_ylim(ylimits[0], ylimits[1])
    axs.grid(True)
    axs.set_title(title)
    axs.plot(error)
    axs.legend(['Error (m)'], loc='upper right')


if __name__ == "__main__":
    # Use file
    left = "result_distance_1_devices_1_path_4_Nikkei_unweighted.csv"
    right = "result_distance_1_devices_1_path_4_Nikkei_weighted.csv"

    fig = plt.figure(figsize=plt.figaspect(.5))
    fig.suptitle(f"Estimated locations for location [-1, 0] with Nikkei")
    limits = [-2.5, 0.5, -2, 1]
    axs = fig.add_subplot(1, 2, 1)
    axs2 = fig.add_subplot(1, 2, 2)

    make_scatter_plot(axs, left, [-1, 0], limits, title="Unweighted")
    make_scatter_plot(axs2, right, [-1, 0], limits, title="Weighted")

    plt.savefig("render/nikkei_location.pdf")

    plt.show()

    fig = plt.figure(figsize=plt.figaspect(.5))
    fig.suptitle(f"RMSE over measurements for location [-1, 0] with Nikkei")
    ylimits = [0.5,2]
    axs = fig.add_subplot(1, 2, 1)
    axs2 = fig.add_subplot(1, 2, 2)

    make_error_plot(axs, left, [-1, 0], ylimits, title="Unweighted")
    make_error_plot(axs2, right, [-1, 0], ylimits, title="Weighted")

    plt.savefig("render/nikkei_error.pdf")

    # do the same for 5 distance

    left = "result_distance_5_devices_1_path_4_Nikkei_unweighted.csv"
    right = "result_distance_5_devices_3_path_4_Nikkei_unweighted.csv"

    fig = plt.figure(figsize=plt.figaspect(.5))
    fig.suptitle(f"Estimated locations for location [0, 5] with Nikkei")
    limits = [-4.5, 0.2, -2, 8]
    axs = fig.add_subplot(1, 2, 1)
    axs2 = fig.add_subplot(1, 2, 2)

    make_scatter_plot(axs, left, [0,5], limits, title="One device streaming, unweighted")
    make_scatter_plot(axs2, right, [0,5], limits, title="Three devices streaming, unweighted")

    plt.savefig("render/nikkei_location_5.pdf")

    fig = plt.figure(figsize=plt.figaspect(.5))
    fig.suptitle(f"RMSE over measurements for location [0, 5] with Nikkei")
    ylimits = [5, 7.5]
    axs = fig.add_subplot(1, 2, 1)
    axs2 = fig.add_subplot(1, 2, 2)

    make_error_plot(axs, left, [0,5], ylimits, title="One device streaming, unweighted")
    make_error_plot(axs2, right, [0,5], ylimits, title="Three devices streaming, unweighted")

    plt.savefig("render/nikkei_error_5.pdf")
