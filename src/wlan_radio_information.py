import pandas as pd

class WlanRadioInformation:
    def __init__(self, signals=None, data_rate=None, radio_timestamp=None, frequency_mhz=None):
        self.signals = signals
        self.data_rate = data_rate
        self.radio_timestamp = radio_timestamp
        self.frequency_mhz = frequency_mhz

    @classmethod
    def from_layer(cls, layer, wifi_card, sniff_timestamp):
        """
            Parses the wlan_radio layer and constructs a WlanRadioInformation object

        :param layer: Layer from pyshark
        """
        signal_strength = layer.get("wlan_radio.signal_dbm")
        signal_strength = float(signal_strength) if signal_strength is not None else None
        signals = [{'signal_strength': signal_strength, **wifi_card, 'sniff_timestamp': sniff_timestamp}]
        data_rate = layer.get("wlan_radio.data_rate")
        data_rate = float(data_rate) if data_rate is not None else None
        radio_timestamp = layer.get("wlan_radio.timestamp")
        radio_timestamp = int(radio_timestamp) if radio_timestamp is not None else None
        frequency_mhz  = layer.get("wlan_radio.frequency")
        frequency_mhz = int(frequency_mhz) if frequency_mhz is not None else None
        return cls(signals, data_rate, radio_timestamp, frequency_mhz)

    def __eq__(self, other):
        """
            Overrides the default implementation
            Don't compare signal_strength
        :param other:
        :return:
        """
        return self.data_rate == other.data_rate \
            and self.radio_timestamp == other.radio_timestamp \
            and self.frequency_mhz == other.frequency_mhz

    def __key__(self):
        """
            Overrides the default implementation
            Don't compare signal_strength
        :param other:
        :return:
        """
        return self.data_rate, self.radio_timestamp, self.frequency_mhz

    def __hash__(self):
        return hash(self.__key__())

    def get_earliest_sniff_timestamp(self):
        """
            Returns the earliest timestamp of all the signals
        """
        return min(signal['sniff_timestamp'] for signal in self.signals)

    def to_dict(self): 
        return {
            'signals': self.signals,
            'data_rate': self.data_rate,
            'radio_timestamp': self.radio_timestamp,
            'frequency_mhz': self.frequency_mhz
        }

    def to_dataframe(self):
        df = pd.DataFrame({'signal_strength': [self.signals[0]['signal_strength']], 'location': [self.signals[0]['location']], 'sniff_timestamp': [self.signals[0]['sniff_timestamp']]})
        for i in range(1, len(self.signals)):
            newDf = pd.DataFrame({'signal_strength': [self.signals[i]['signal_strength']], 'location': [self.signals[i]['location']], 'sniff_timestamp': [self.signals[i]['sniff_timestamp']]})
            df = df.join(newDf, rsuffix='_'+ str(i))
        df['data_rate'] = self.data_rate
        df['radio_timestamp'] = self.radio_timestamp
        df['frequency_mhz'] = self.frequency_mhz
        return df