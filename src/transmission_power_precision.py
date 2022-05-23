from sympy import Point2D

from src.data_generators.location_data_generator import LocationGenerator
from src.device.device import Device
from src.location.average_signal_strength import average_signals
from src.location.multi_lateration_non_linear_least_square_sum import calculate_position


def average_error():
    wifi_frame_generator = LocationGenerator([Point2D([0, 4.33]), Point2D([5, -4.33]), Point2D([-5, -4.33])],
                                             rounding=False)
    path_loss_exponent = 4

    max_distance = 10
    distance_step = 1

    tx_power_max = 20
    tx_power_min = -20
    tx_power_actual = [-10, 10]
    tx_power_step = 0.5

    for tx_power in tx_power_actual:
        distance_current = 0

        tx_power_current = tx_power_min

        power_points_dict = {}

        print("Making dict")
        while tx_power_current <= tx_power_max:
            power_points_dict[tx_power_current] = []
            tx_power_current = tx_power_current + tx_power_step

        tx_power_current = tx_power_min

        print("Making list of list of points")
        while distance_current <= max_distance:
            wifi_frame = wifi_frame_generator.make_wifi_element(Point2D([0, distance_current]),
                                                                transmission_power_dbm=tx_power)
            device = Device("0", [wifi_frame])

            signal_strengths = []

            for frame in device.frames:
                signal_strengths.append(frame.wlan_radio.signals)

            device.averaged_signals = average_signals(signal_strengths)

            while tx_power_current <= tx_power_max:
                calculate_position(device, path_loss_exponent, tx_power_current, 0)

                power_points_dict[tx_power_current].append(device.position)

                tx_power_current = tx_power_current + tx_power_step

            distance_current = distance_current + distance_step
            tx_power_current = tx_power_min

        distance_current = 0

        print("Calculate errors")
        for key in power_points_dict.keys():
            error_sum = float(0)
            for estimated_point in power_points_dict[key]:
                actual_point = Point2D([0, distance_current])
                error_sum = error_sum + float(Point2D(estimated_point).distance(actual_point))
                distance_current = distance_current + distance_step

            distance_current = 0

            print(f"{tx_power}\t{key}\t{error_sum / len(power_points_dict[key])}")


def error_at_distance(distance):
    wifi_frame_generator = LocationGenerator([Point2D([0, 4.33]), Point2D([5, -4.33]), Point2D([-5, -4.33])],
                                             rounding=False)
    path_loss_exponent = 4
    actual_point = Point2D([0, distance])

    tx_power_max = 100
    tx_power_min = -100
    tx_power_actual = [-100, 100]
    tx_power_step = 0.5

    for tx_power in tx_power_actual:
        wifi_frame = wifi_frame_generator.make_wifi_element(Point2D([0, distance]),
                                                            transmission_power_dbm=tx_power)
        device = Device("0", [wifi_frame])

        signal_strengths = []

        for frame in device.frames:
            signal_strengths.append(frame.wlan_radio.signals)

        device.averaged_signals = average_signals(signal_strengths)

        tx_power_current = tx_power_min

        while tx_power_current <= tx_power_max:
            calculate_position(device, path_loss_exponent, tx_power_current, 0)

            error = float(Point2D(device.position).distance(actual_point))

            print(f"{tx_power}\t{tx_power_current}\t{error}")

            tx_power_current = tx_power_current + tx_power_step


if __name__ == '__main__':
    # average_error()


    error_at_distance(10)
