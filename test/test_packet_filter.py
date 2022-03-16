from src.packet_filter import PacketFilter
from src.wifi_frame import WifiFrame


def test_packet_filter_subtype_allowed():
    assert PacketFilter.filter_packets_by_subtypes(
        WifiFrame(), [0]
    ) is True
