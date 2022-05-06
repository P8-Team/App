from __future__ import annotations

import pandas as pd

from src.wifi.signal import Signal
from src.wifi.wifi_card import WifiCard


class WlanRadioInformation:
    signals: list[Signal]
    data_rate: float
    radio_timestamp: float
    frequency_mhz: int

    def __init__(self, signals: list[Signal] = None, data_rate: float = None, radio_timestamp: float = None,
                 frequency_mhz: int = None):
        self.signals = signals
        self.data_rate = data_rate
        self.radio_timestamp = radio_timestamp
        self.frequency_mhz = frequency_mhz

    @classmethod
    def from_layer(cls, layer, wifi_card: WifiCard, sniff_timestamp: float) -> WlanRadioInformation:
        """
            Parses the wlan_radio layer and constructs a WlanRadioInformation object

        :param layer: Layer from pyshark
        :param wifi_card: WifiCard object it was sniffed on
        :param sniff_timestamp: Local timestamp it was sniffed at
        """
        signal_strength = layer.get("wlan_radio.signal_dbm")
        signal_strength = float(signal_strength) if signal_strength is not None else None
        signals = [Signal(wifi_card.location, signal_strength, sniff_timestamp)]
        data_rate = layer.get("wlan_radio.data_rate")
        data_rate = float(data_rate) if data_rate is not None else None
        radio_timestamp = layer.get("wlan_radio.timestamp")
        radio_timestamp = int(radio_timestamp) if radio_timestamp is not None else None
        frequency_mhz = layer.get("wlan_radio.frequency")
        frequency_mhz = int(frequency_mhz) if frequency_mhz is not None else None
        return cls(signals, data_rate, radio_timestamp, frequency_mhz)

    def __eq__(self, other: WlanRadioInformation) -> bool:
        """
            Overrides the default implementation
            Don't compare signal_strength
        :param other:
        :return:
        """
        return self.data_rate == other.data_rate \
               and self.radio_timestamp == other.radio_timestamp \
               and self.frequency_mhz == other.frequency_mhz

    def __key__(self) -> tuple:
        """
            Overrides the default implementation
            Don't compare signal_strength
        """
        return self.data_rate, self.radio_timestamp, self.frequency_mhz

    def __hash__(self) -> int:
        return hash(self.__key__())

    def get_earliest_sniff_timestamp(self) -> float:
        """
            Returns the earliest timestamp of all the signals
        """
        return min(signal.sniff_timestamp for signal in self.signals)

    def get_smallest_timestamp_delta(self) -> float | None:
        signals_with_timestamp_delta = [signal for signal in self.signals if signal.timestamp_delta != None]
        if not signals_with_timestamp_delta:
            return None
        else:
            return min(signal.timestamp_delta for signal in signals_with_timestamp_delta)

    def to_dataframe(self):

        all_timestamp_deltas_none = all(signal.timestamp_delta == None for signal in self.signals)

        minimum_timestamp_delta = None if all_timestamp_deltas_none \
                                       else min(signal.timestamp_delta for signal in self.signals)
        df = pd.DataFrame(data=
        {
            'timestamp_delta': [minimum_timestamp_delta],
            'data_rate': [self.data_rate], 'radio_timestamp': [self.radio_timestamp], 'frequency_mhz': [self.frequency_mhz]
        })

        return df
