from __future__ import annotations

import json
import pandas as pd
from typing import Generator, Iterator

from src.wifi.frame_control_information import FrameControlInformation
from src.wifi.wifi_card import WifiCard
from src.wifi.wlan_radio_information import WlanRadioInformation

class WifiFrame:
    """
        The data structure used internally to represent WiFi-frames as they appear from the physical layer
        Most attributes are removed when constructed, leaving only attributes that can be relevant for further analysis.
    """
    frame_control_information: FrameControlInformation
    wlan_radio: WlanRadioInformation
    length: int
    fcs: int

    def __init__(self, length: int = None, fcs: int = None, wlan_radio: WlanRadioInformation = None,
                 frame_control_information: FrameControlInformation = None):
        self.frame_control_information = frame_control_information
        self.length = length
        self.wlan_radio = wlan_radio
        self.fcs = fcs

    @classmethod
    def from_frame(cls, frame, wifi_card: WifiCard) -> WifiFrame:
        length = int(frame.length)
        fcs = frame.wlan.get("fcs")
        # print as integer
        if fcs is not None:
            fcs = int(fcs, 16)
        sniff_timestamp = float(frame.sniff_timestamp)
        wlan_radio = WlanRadioInformation.from_layer(frame.wlan_radio, wifi_card, sniff_timestamp)
        frame_control_information = FrameControlInformation.from_layer(frame.wlan)
        return cls(length, fcs, wlan_radio, frame_control_information)

    def __eq__(self, other: WifiFrame) -> bool:
        """
            Overrides the default implementation
            Compares everything but sniff_timestamp and signal_strength, as everything else should be the same for the same frame.
        :param other:
        :return: boolean
        """
        return self.frame_control_information == other.frame_control_information and \
               self.length == other.length and \
               self.wlan_radio == other.wlan_radio and \
               self.fcs == other.fcs

    def __repr__(self) -> str:
        """
            Converts the object to a json string
            Used for debugging purposes
        :return:
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @classmethod
    def construct_from_generator(cls, generator: Generator) -> Iterator[WifiFrame]:
        for frame in generator:
            yield cls(frame)

    def __key__(self) -> tuple:
        """
            Returns a tuple of all attributes that are used for comparison
            Calls __key__ on the frame_control_information object to avoid getting signal_strength in the comparison
        :return:
        """
        return self.length, self.fcs, self.frame_control_information, self.wlan_radio.__key__()

    def __hash__(self) -> int:
        return hash(self.__key__())

    def to_dataframe(self):
        len_df = pd.DataFrame({'length': [self.length]})
        return pd.concat([len_df, self.wlan_radio.to_dataframe(), self.frame_control_information.to_dataframe()], axis = 1)

