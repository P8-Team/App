import re
from datetime import *


def mac_address_validator(address: str):
    # Regex found on https://ihateregex.io/expr/mac-address/
    if re.search("^[a-fA-F0-9]{2}(:[a-fA-F0-9]{2}){5}$", address):
        return address
    else:
        raise TypeError("Incorrect Mac Address Formatting")


class Packet:
    identifier = 0

    def __init__(self, mac_address, packet_length, RSSI):
        self.packet_length = packet_length
        self.mac_address = mac_address_validator(mac_address)
        self.RSSI = RSSI
        Packet.identifier += 1
        self.identifier = Packet.identifier
        self.distance = 0
        self.angle = 0
        self.timeStamp = datetime.now()
