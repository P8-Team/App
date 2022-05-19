from __future__ import annotations

import json
from typing import Generator, Iterator

import pandas as pd
from sympy import Point2D, N

from src.wifi.frame_control_information import FrameControlInformation
from src.wifi.signal import Signal
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
    frame_control_sequence: int

    def __init__(self, length: int = None, frame_control_sequence: int = None, wlan_radio: WlanRadioInformation = None,
                 frame_control_information: FrameControlInformation = None):
        self.frame_control_information = frame_control_information
        self.length = length
        self.wlan_radio = wlan_radio
        self.frame_control_sequence = frame_control_sequence

    @classmethod
    def from_frame(cls, frame, wifi_card: WifiCard) -> WifiFrame:
        length = int(frame.length)
        frame_control_sequence = frame.wlan.get("fcs")
        # print as integer
        if frame_control_sequence is not None:
            frame_control_sequence = int(frame_control_sequence, 16)
        sniff_timestamp = float(frame.sniff_timestamp)
        wlan_radio = WlanRadioInformation.from_layer(frame.wlan_radio, wifi_card, sniff_timestamp)
        frame_control_information = FrameControlInformation.from_layer(frame.wlan)
        return cls(length, frame_control_sequence, wlan_radio, frame_control_information)

    def __eq__(self, other: WifiFrame) -> bool:
        """
            Overrides the default implementation
            Compares everything but sniff_timestamp and signal_strength, as everything else should be the same for the same frame.
        :param other:
        :return: boolean
        """
        return other is not None and \
               self.frame_control_information == other.frame_control_information and \
               self.length == other.length and \
               self.wlan_radio == other.wlan_radio and \
               self.frame_control_sequence == other.frame_control_sequence

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
        return self.length, self.frame_control_sequence, self.frame_control_information.__key__(), self.wlan_radio.__key__()

    def __hash__(self) -> int:
        return hash(self.__key__())

    def to_dataframe(self):
        len_df = pd.DataFrame({'length': [self.length]})
        return pd.concat([len_df, self.wlan_radio.to_dataframe(), self.frame_control_information.to_dataframe()],
                         axis=1)

    @staticmethod
    def get_csv_header():
        return "length,frame_control_sequence,card_location_x,card_location_y,signal_strength,sniff_timestamp,"\
               "data_rate,radio_timestamp,frequency_mhz,type,subtype,receiver_address,transmitter_address"

    def to_csv_row(self):
        return f"{self.length},{self.frame_control_sequence},{self.wlan_radio.signals[0].location.x}," \
          f"{self.wlan_radio.signals[0].location.y},{self.wlan_radio.signals[0].signal_strength}," \
          f"{self.wlan_radio.signals[0].sniff_timestamp},{self.wlan_radio.data_rate},"\
          f"{self.wlan_radio.radio_timestamp},{self.wlan_radio.frequency_mhz},{self.frame_control_information.type},"\
          f"{self.frame_control_information.subtype},{self.frame_control_information.receiver_address}," \
          f"{self.frame_control_information.transmitter_address}"

    @classmethod
    def from_csv_row(cls, row: str):
        row_split = row.strip().split(",")
        length = int(row_split[0])
        frame_control_sequence = int(row_split[1])
        card_location_x = N(row_split[2])
        card_location_y = N(row_split[3])
        signal_strength = None if row_split[4] == 'None' else float(row_split[4])
        sniff_timestamp = float(row_split[5])
        data_rate = float(row_split[6])
        radio_timestamp = None
        frequency_mhz = int(row_split[8])
        fc_type = int(row_split[9])
        subtype = int(row_split[10])
        receiver_address = row_split[11]
        transmitter_address = row_split[12]

        wlan_radio = WlanRadioInformation(
            [Signal(Point2D(card_location_x, card_location_y), signal_strength, sniff_timestamp)],
            data_rate, radio_timestamp, frequency_mhz
        )

        frame_control_information = FrameControlInformation(fc_type, subtype, receiver_address, transmitter_address)

        return cls(length, frame_control_sequence, wlan_radio, frame_control_information)
