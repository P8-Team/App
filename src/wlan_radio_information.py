class WlanRadioInformation:
    def __init__(self, signal_strength=None, data_rate=None, radio_timestamp=None):
        self.signal_strength = signal_strength
        self.data_rate = data_rate
        self.radio_timestamp = radio_timestamp

    @classmethod
    def from_layer(cls, layer):
        """
            Parses the wlan_radio layer and constructs a WlanRadioInformation object

        :param layer: Layer from pyshark
        """
        signal_strength = layer.get("wlan_radio.signal_dbm")
        signal_strength = float(signal_strength) if signal_strength is not None else None
        data_rate = layer.get("wlan_radio.data_rate")
        data_rate = float(data_rate) if data_rate is not None else None
        radio_timestamp = layer.get("wlan_radio.timestamp")
        radio_timestamp = int(radio_timestamp) if radio_timestamp is not None else None
        return cls(signal_strength, data_rate, radio_timestamp)

    def __eq__(self, other):
        """
            Overrides the default implementation
            Don't compare signal_strength
        :param other:
        :return:
        """
        return self.data_rate == other.data_rate \
            and self.radio_timestamp == other.radio_timestamp

    def __key__(self):
        """
            Overrides the default implementation
            Don't compare signal_strength
        :param other:
        :return:
        """
        return self.data_rate, self.radio_timestamp

    def __hash__(self):
        return hash(self.__key__())


        