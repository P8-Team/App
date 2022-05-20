from sympy import Point2D

from src.data_generators.location_data_generator import LocationGenerator
from src.device.device import Device
from src.location.average_signal_strength import average_signals
from src.location.multi_lateration_non_linear_least_square_sum import calculate_position

if __name__ == '__main__':

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

# -20: 37.44436243244219
# -19.5: 36.75656257726219
# -19.0: 36.09613077431512
# -18.5: 35.67628965178895
# -18.0: 35.02299263459019
# -17.5: 34.20932990538222
# -17.0: 33.76089183387972
# -16.5: 32.94841593682644
# -16.0: 32.37475838148333
# -15.5: 31.684153892957415
# -15.0: 31.022537689725986
# -14.5: 30.186142770281425
# -14.0: 29.555836616828774
# -13.5: 28.81778159635618
# -13.0: 28.04075057291923
# -12.5: 27.2291342880585
# -12.0: 26.431646126314313
# -11.5: 25.582460765446037
# -11.0: 24.812695800509882
# -10.5: 23.92488506118917
# -10.0: 23.108005857465105
# -9.5: 22.182388109190484
# -9.0: 21.255534234488472
# -8.5: 20.33518929322353
# -8.0: 19.34155012674581
# -7.5: 18.328291519642192
# -7.0: 17.331013875973962
# -6.5: 16.26950507245414
# -6.0: 15.228404654348086
# -5.5: 14.130037240263905
# -5.0: 13.026845740663877
# -4.5: 11.891572717968472
# -4.0: 10.700281008928608
# -3.5: 9.49175941184772
# -3.0: 8.259634058959215
# -2.5: 6.9676455952268
# -2.0: 5.656322552852464
# -1.5: 4.294797321239607
# -1.0: 2.9057630960757277
# -0.5: 1.4711763322132545
# 0.0: 5.2914405113292876e-05
# 0.5: 1.516683191882019
# 1.0: 3.074808870265846
# 1.5: 4.6782888450976365
# 2.0: 6.328450558504032
# 2.5: 8.026654081520277
# 3.0: 9.786735012520705
# 3.5: 11.585578008789296
# 4.0: 13.43680029514331
# 4.5: 15.365812320059966
# 5.0: 17.327014412249973
# 5.5: 19.345334464640636
# 6.0: 21.422442082346095
# 6.5: 23.56005553907695
# 7.0: 25.759941210735647
# 7.5: 28.06432624359582
# 8.0: 30.395227006528987
# 8.5: 32.79403870503043
# 9.0: 35.26274240908326
# 9.5: 37.80337596619639
# 10.0: 40.4757960618442
# 10.5: 43.16871812722387
# 11.0: 45.940007788604554
# 11.5: 48.792004352640106
# 12.0: 51.72703004894886
# 12.5: 54.74885157281541
# 13.0: 57.857044393341205
# 13.5: 61.0558606779527
# 14.0: 64.3479231449691
# 14.5: 67.73596193488757
# 15.0: 71.22279456313996
# 15.5: 74.81129971825703
# 16.0: 78.50442846537739
# 16.5: 82.30527175488783
# 17.0: 86.21696720528041
# 17.5: 90.24274711851928
# 18.0: 94.3859387380755
# 18.5: 98.64998535941857
# 19.0: 103.03842116670181
# 19.5: 107.5548680865827
# 20.0: 112.20306125662633
