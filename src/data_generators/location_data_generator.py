from sympy import Point2D

from src.location.distance_strength_calculations import mw_to_dbm, distance_to_signal_strength_free_space_path_loss, \
    distance_to_signal_strength
from src.wifi.frame_control_information import FrameControlInformation
from src.wifi.signal import Signal
from src.wifi.wifi_frame import WifiFrame
from src.wifi.wlan_radio_information import WlanRadioInformation


class LocationGenerator:
    receiver_positions: list[Point2D]
    path_loss_exponent: float

    def __init__(self, receiver_positions: list[Point2D], rounding=True, path_loss_exponent=4):
        """

        :param receiver_positions: List of positions for receivers
        """
        self.receiver_positions = []
        self.rounding = rounding
        self.path_loss_exponent = path_loss_exponent
        self._positions_populator(receiver_positions)

    def make_wifi_element(self, position: Point2D, frequency=2412, transmission_power_dbm=20,
                          transmitter_address="00:00:00:00:00:01", receiver_address="00:00:00:00:00:02", sniff_timestamp=0):
        """

        :param position: The position of the transmitter, given as a sympy Point
        :param frequency: Frequency in mhz
        :param transmission_power_dbm: Transmission power of the transmitter, defaults to 20, given in dBm
        :param transmitter_address: The physical address of the device that transmitted the frame
        :param receiver_address: The physical address of the device that received the frame
        :return: Returns a new wifi_element containing the relevant information to generate calculate locations
        """
        if not frequency > 0:
            raise ValueError("Frequency should be greater than 0")

        wifi_element = WifiFrame(frame_control_sequence=1,
                                 frame_control_information=FrameControlInformation(
                                     transmitter_address=transmitter_address,
                                     receiver_address=receiver_address, fc_type=1, subtype=1), length=2)
        signal_strength = self.signal_strength_calculator(position, transmission_power_dbm)

        signals = [Signal(element[0], element[1], sniff_timestamp) for element in zip(self.receiver_positions, signal_strength)]
        data_rate = None
        timestamp = None
        wifi_element.wlan_radio = WlanRadioInformation(signals, data_rate, timestamp, frequency)
        return wifi_element

    def _positions_populator(self, positions):
        for element in positions:
            if not isinstance(element, Point2D):
                raise TypeError("Element is not a Point")
            self.receiver_positions.append(element)

    def signal_strength_calculator(self, point: Point2D, transmission_power):
        output = []
        for pos in self.receiver_positions:
            signal_strength = distance_to_signal_strength(point.distance(pos), transmission_power,
                                                          self.path_loss_exponent)

            if self.rounding:
                output.append(round(signal_strength))
            else:
                output.append(signal_strength)

        return output
