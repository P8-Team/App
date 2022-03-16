class WlanRadioInformation:
    def __init__(self, layer):
        rssi = layer.get("wlan_radio.signal_dbm")
        self.rssi = int(rssi) if rssi is not None else None
        data_rate = layer.get("wlan_radio.data_rate")
        self.data_rate = int(data_rate) if data_rate is not None else None
        radio_timestamp = layer.get("wlan_radio.timestamp")
        self.radio_timestamp = int(radio_timestamp) if radio_timestamp is not None else None

    def __eq__(self, other):
        """
            Overrides the default implementation
            Don't compare RSSI
        :param other:
        :return:
        """
        return self.data_rate == other.data_rate \
            and self.radio_timestamp == other.radio_timestamp

        