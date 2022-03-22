from src.frame_control_information import FrameControlInformation
from src.packet_filter import PacketFilter
from src.wifi_frame import WifiFrame


def get_packet_filter():
    packet_filter = PacketFilter()
    packet_filter.whitelisted_types = [0]
    packet_filter.whitelisted_subtypes = [2, 3, 4]
    return packet_filter


def get_wifi_frame(fc_type, subtype):
    frame_control_information = FrameControlInformation(fc_type, subtype)
    return WifiFrame(0, 0, None, frame_control_information)


def test_packet_filter_subtype_allowed():
    packet_filter = get_packet_filter()
    wifi_frame = get_wifi_frame(0, 2)
    assert packet_filter.filter_packets_by_subtypes(wifi_frame, [2])


def test_packet_filter_subtype_disallowed():
    packet_filter = get_packet_filter()
    wifi_frame = get_wifi_frame(0, 3)
    assert not packet_filter.filter_packets_by_subtypes(wifi_frame, [2])


def test_packet_filter_subtype_none():
    packet_filter = get_packet_filter()
    wifi_frame = get_wifi_frame(0, None)
    assert not packet_filter.filter_packets_by_subtypes(wifi_frame, [2])


def test_packet_filter_type_allowed():
    packet_filter = get_packet_filter()
    wifi_frame = get_wifi_frame(0, 2)
    assert packet_filter.packet_types_filter_func(wifi_frame, [0])


def test_packet_filter_type_disallowed():
    packet_filter = get_packet_filter()
    wifi_frame = get_wifi_frame(1, 2)
    assert not packet_filter.packet_types_filter_func(wifi_frame, [0])


def test_packet_filter_type_none():
    packet_filter = get_packet_filter()
    wifi_frame = get_wifi_frame(None, 2)
    assert not packet_filter.packet_types_filter_func(wifi_frame, [0])


def test_filter_on_generator_allowed():
    packet_filter = get_packet_filter()
    wifi_frame = get_wifi_frame(0, 2)
    assert list(packet_filter.filter([wifi_frame]))[0] == wifi_frame


def test_filter_on_generator_disallowed():
    packet_filter = get_packet_filter()
    wifi_frame = get_wifi_frame(1, 2)
    assert len(list(packet_filter.filter([wifi_frame]))) == 0


def test_filter_on_generator_none():
    packet_filter = get_packet_filter()
    wifi_frame = get_wifi_frame(None, None)
    assert len(list(packet_filter.filter([wifi_frame]))) == 0


def test_filter_on_generator_mixed_multiple():
    packet_filter = get_packet_filter()
    wifi_frames = [
        get_wifi_frame(0, 2),
        get_wifi_frame(1, 2),
        get_wifi_frame(0, 3),
        get_wifi_frame(1, 3),
    ]

    result = list(packet_filter.filter(wifi_frames))

    assert len(result) == 2
    assert result[0] == wifi_frames[0]
    assert result[1] == wifi_frames[2]
