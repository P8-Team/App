import math

from sympy import Point

from src.distance_strength_calculations import mw_to_dbm, wavelength
from src.wifi_frame import WifiFrame
from src.wlan_radio_information import WlanRadioInformation


class LocationGenerator:
    def __init__(self, receiver_positions: list):
        """

        :param receiver_positions: List of positions for receivers
        """
        self.receiver_positions = []
        self._positions_populator(receiver_positions)

    def generator(self, position: Point, frequency, transmission_power=100):
        """

        :param position: The position of the transmitter, given as a sympy Point
        :param frequency: Frequency in mhz
        :param transmission_power: Transmission power of the transmitter, defaults to 100
        :return: Returns a new wifi_element containing the relevant information to generate calculate locations
        """
        if not frequency > 0:
            raise ValueError("Frequency should be greater than 0")

        wifi_element = WifiFrame()
        signal_strength = self.signal_strength_calculator(position, frequency, transmission_power)
        data_rate = []
        timestamp = []
        wifi_element.wlan_radio = WlanRadioInformation(signal_strength, data_rate, timestamp)
        yield wifi_element

    def _positions_populator(self, positions):
        for element in positions:
            if not isinstance(element, Point):
                raise TypeError("Element is not a Point")
            self.receiver_positions.append(element)

    def signal_strength_calculator(self, point: Point, frequency, transmission_power):
        output = []
        for pos in self.receiver_positions:
            signal_strength = distance_to_signal_strength(point.distance(pos), frequency, transmission_power)

            output.append(round((mw_to_dbm(signal_strength))))

        return output


def distance_to_signal_strength(distance, frequency, transmission_power):
    if not distance > 0:
        raise TypeError("Distance should be more than 0")
    wl = wavelength(frequency)

    return (transmission_power * pow(wl, 2)) / pow(4 * math.pi * distance, 2)
