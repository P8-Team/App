class PacketFilter:

    def __init__(
            self,
            whitelisted_types=None,
            whitelisted_subtypes=None
    ):
        # https://en.wikipedia.org/wiki/802.11_Frame_Types
        if whitelisted_types is None:
            whitelisted_types = [2]
        if whitelisted_subtypes is None:
            whitelisted_subtypes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.whitelisted_types = whitelisted_types
        self.whitelisted_subtypes = whitelisted_subtypes

    def filter(self, iterator):
        """
            Filters the iterator for types/subtypes not in whitelist.
        :param iterator:
        :return:
        """
        return self.filter_iterator(iterator,
                                    lambda packet:
                                    self.filter_packets_by_subtypes(packet, self.whitelisted_subtypes)
                                    and self.packet_types_filter_func(packet, self.whitelisted_types)
                                    )

    @staticmethod
    def filter_iterator(iterator, filter_func):
        """
            Filters a packet iterator using a filter function.

        :param iterator:
        :param filter_func:
        :return:
        """
        for packet in iterator:
            if filter_func(packet):
                yield packet

    @staticmethod
    def packet_types_filter_func(packet, types):
        return packet.frame_control_information.type in types

    @staticmethod
    def filter_packets_by_subtypes(packet, subtypes):
        return packet.frame_control_information.subtype in subtypes
