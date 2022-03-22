class FrameControlInformation:
    def __init__(self, fc_type=None, subtype=None, receiver_address=None, transmitter_address=None):
        self.type = fc_type
        self.subtype = subtype
        self.receiver_address = receiver_address
        self.transmitter_address = transmitter_address

    @classmethod
    def from_layer(cls, layer):
        """
            Parses the wlan layer and constructs a FrameControlInformation object

        :param layer: Layer from pyshark
        """
        fc_type = layer.get('wlan.fc.type')
        fc_type = int(fc_type) if fc_type else None
        subtype = layer.get('wlan.fc.subtype')
        subtype = int(subtype) if subtype else None
        receiver_address = layer.get('wlan.ra_resolved')
        transmitter_address = layer.get('wlan.ta_resolved')
        return cls(fc_type, subtype, receiver_address, transmitter_address)

    def __eq__(self, other):
        return self.type == other.type \
               and self.subtype == other.subtype \
               and self.receiver_address == other.receiver_address \
               and self.transmitter_address == other.transmitter_address

    def __key__(self):
        return self.type, self.subtype, self.receiver_address, self.transmitter_address

    def __hash__(self):
        return hash(self.__key__())
