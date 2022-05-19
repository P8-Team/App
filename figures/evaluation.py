from os import listdir
from os.path import isfile, join

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def get_devices_from_path(path):
    # get the first char after 'devices_' as int
    index = path.find('devices_') + 8
    return int(path[index:index+1])


def get_weighted(path):
    return path.find('weighted') != -1


def euclidean_distance(x, y, expected_location):
    # create new list of distances
    distances = []
    for i in range(len(x)):
        distances.append(np.sqrt((x[i] - expected_location[0]) ** 2 + (y[i] - expected_location[1]) ** 2))
    return distances


def make_result(path, expected_location):
    print("Path: " + path)
    data = pd.read_csv(join("results", path), sep=',')

    fig = plt.figure(figsize=plt.figaspect(.5))
    fig.suptitle(f"{data['identification_transmit_power'][0]} for location {expected_location}"
              f" with {get_devices_from_path(path)} devices, {'weighted' if get_weighted(path) else 'unweighted'}")
    axs = fig.add_subplot(1, 2, 1)
    axs2 = fig.add_subplot(1, 2, 2)

    x = data['x'].to_list()
    y = data['y'].to_list()
    axs.scatter(expected_location[0], expected_location[1], c='black', marker='x')
    axs.scatter(x, y, s=1)
    # add legend
    axs.legend(['Actual Location', 'Estimated locations'], loc='upper right')
    axs.set_xlabel('x (m)')
    axs.set_ylabel('y (m)')
    axs.grid(True)
    axs.set_title(f"Estimations of location")

    error = euclidean_distance(x, y, expected_location)
    axs2.set_xlabel('measurement #')
    axs2.set_ylabel(f'error (euclidean distance in meters to {expected_location})')
    axs2.grid(True)
    axs2.set_title(f"Error of estimations over measurements")
    axs2.plot(error)
    axs2.legend(['Error (m)'], loc='upper right')

    # plt.show()
    plt.savefig(f"render/{path.rstrip('.csv')}.pdf")

    # calculate mean error and RMSE
    mean_error = np.mean(error)
    rmse = 1/ len(error) * np.sum(error)
    print("Mean error: ", mean_error)
    print("RMSE: ", rmse)


if __name__ == "__main__":
    # Find all the files in the folder
    files = [f for f in listdir("results") if isfile(join("results", f)) and f.endswith(".csv")]

    # Render pr files
    for file in files:
        # find the string that comes after distance_
        distance_location = file.find("distance_")
        device_location = file.find("devices_")
        distance = int(file[distance_location + len("distance_"):device_location - 1])

        if distance == 1:
            expected_location = [-1, 0]
        elif distance == 5:
            expected_location = [0, 5]
        elif distance == 10:
            expected_location = [0, 10]
        else:
            raise Exception("Distance not supported")

        make_result(file, expected_location)
