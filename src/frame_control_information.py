import json


class FrameControlInformation:
    def __init__(self, layer):
        """
            Parses the wlan layer and constructs a FrameControlInformation object

        :param frame: Frame from pyshark
        """
        self.type = layer.get('wlan.fc.type')
        self.subtype = layer.get('wlan.fc.subtype')
        self.receiver_address = layer.get('wlan.ra_resolved', '<unknown>')
        self.transmitter_address = layer.get('wlan.ta_resolved', '<unknown>')
