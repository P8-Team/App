class WlanRadioInformation:
    def __init__(self, layer):
        self.rssi = int(layer.get("wlan_radio.signal_dbm"))
        self.data_rate = int(layer.get("wlan_radio.data_rate"))
        self.radio_timestamp = int(layer.get("wlan_radio.timestamp"))

    def __eq__(self, other):
        """
            Overrides the default implementation
            Don't compare RSSI
        :param other:
        :return:
        """
        return self.data_rate == other.data_rate \
            and self.radio_timestamp == other.radio_timestamp

        