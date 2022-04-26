from sympy import Point2D

from src.location.distance_strength_calculations import mw_to_dbm, distance_to_signal_strength
from src.wifi.frame_control_information import FrameControlInformation
from src.wifi.signal import Signal
from src.wifi.wifi_frame import WifiFrame
from src.wifi.wlan_radio_information import WlanRadioInformation


class LocationGenerator:
    receiver_positions: list[Point2D]

    def __init__(self, receiver_positions: list[Point2D]):
        """

        :param receiver_positions: List of positions for receivers
        """
        self.receiver_positions = []
        self._positions_populator(receiver_positions)

    def make_wifi_element(self, position: Point2D, frequency=2412, transmission_power=100):
        """

        :param position: The position of the transmitter, given as a sympy Point
        :param frequency: Frequency in mhz
        :param transmission_power: Transmission power of the transmitter, defaults to 100
        :return: Returns a new wifi_element containing the relevant information to generate calculate locations
        """
        if not frequency > 0:
            raise ValueError("Frequency should be greater than 0")

        wifi_element = WifiFrame(frame_control_sequence=1,
                                 frame_control_information=FrameControlInformation(transmitter_address="01",
                                                                                   receiver_address="02"))
        signal_strength = self.signal_strength_calculator(position, frequency, transmission_power)

        signals = [Signal(element[0], element[1], 0) for element in zip(self.receiver_positions, signal_strength)]
        data_rate = None
        timestamp = None
        wifi_element.wlan_radio = WlanRadioInformation(signals, data_rate, timestamp, frequency)
        return wifi_element

    def _positions_populator(self, positions):
        for element in positions:
            if not isinstance(element, Point2D):
                raise TypeError("Element is not a Point")
            self.receiver_positions.append(element)

    def signal_strength_calculator(self, point: Point2D, frequency, transmission_power):
        output = []
        for pos in self.receiver_positions:
            signal_strength = distance_to_signal_strength(point.distance(pos), frequency, transmission_power)

            output.append(round((mw_to_dbm(signal_strength))))

        return output
