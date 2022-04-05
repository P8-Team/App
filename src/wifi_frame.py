import json

from src.frame_control_information import FrameControlInformation
from src.wlan_radio_information import WlanRadioInformation


class WifiFrame:
    """
        The data structure used internally to represent WiFi-frames as they appear from the physical layer
        Most attributes are removed when constructed, leaving only attributes that can be relevant for further analysis.
    """

    def __init__(self, length=None, wlan_radio=None, frame_control_information=None):
        self.frame_control_information = frame_control_information
        self.length = length
        self.wlan_radio = wlan_radio

    @classmethod
    def from_frame(cls, frame, wifi_card):
        length = int(frame.length)
        sniff_timestamp = float(frame.sniff_timestamp)
        wlan_radio = WlanRadioInformation.from_layer(frame.wlan_radio, wifi_card, sniff_timestamp)
        frame_control_information = FrameControlInformation.from_layer(frame.wlan)
        return cls(length, wlan_radio, frame_control_information)

    def __eq__(self, other):
        """
            Overrides the default implementation
            Compares everything but sniff_timestamp and signal_strength, as everything else should be the same for the same frame.
        :param other:
        :return: boolean
        """
        return self.frame_control_information == other.frame_control_information and \
               self.length == other.length and \
               self.wlan_radio == other.wlan_radio

    def __repr__(self):
        """
            Converts the object to a json string
            Used for debugging purposes
        :return:
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @classmethod
    def construct_from_generator(cls, generator):
        for frame in generator:
            yield cls(frame)

    def __key__(self):
        """
            Returns a tuple of all attributes that are used for comparison
            Calls __key__ on the frame_control_information object to avoid getting signal_strength in the comparison
        :return:
        """
        return self.length, self.frame_control_information, self.wlan_radio.__key__()

    def __hash__(self):
        return hash(self.__key__())


