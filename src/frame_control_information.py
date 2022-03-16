class FrameControlInformation:
    def __init__(self, layer):
        """
            Parses the wlan layer and constructs a FrameControlInformation object

        :param frame: Frame from pyshark
        """
        fc_type = layer.get('wlan.fc.type')
        self.type = int(fc_type) if fc_type else None
        subtype = layer.get('wlan.fc.subtype')
        self.subtype = int(subtype) if subtype else None
        self.receiver_address = layer.get('wlan.ra_resolved')
        self.transmitter_address = layer.get('wlan.ta_resolved')

    def __eq__(self, other):
        return self.type == other.type \
               and self.subtype == other.subtype \
               and self.receiver_address == other.receiver_address \
               and self.transmitter_address == other.transmitter_address
