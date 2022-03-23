from src.frame_control_information import FrameControlInformation
from src.frame_filter import FrameFilter
from src.wifi_frame import WifiFrame


def get_frame_filter():
    frame_filter = FrameFilter()
    frame_filter.whitelisted_types = [0]
    frame_filter.whitelisted_subtypes = [2, 3, 4]
    return frame_filter


def get_wifi_frame(fc_type, subtype):
    frame_control_information = FrameControlInformation(fc_type, subtype)
    return WifiFrame(0, 0, None, frame_control_information)


def test_frame_filter_subtype_allowed():
    frame_filter = get_frame_filter()
    wifi_frame = get_wifi_frame(0, 2)
    assert frame_filter.filter_frames_by_subtypes(wifi_frame, [2])


def test_frame_filter_subtype_disallowed():
    frame_filter = get_frame_filter()
    wifi_frame = get_wifi_frame(0, 3)
    assert not frame_filter.filter_frames_by_subtypes(wifi_frame, [2])


def test_frame_filter_subtype_none():
    frame_filter = get_frame_filter()
    wifi_frame = get_wifi_frame(0, None)
    assert not frame_filter.filter_frames_by_subtypes(wifi_frame, [2])


def test_frame_filter_type_allowed():
    frame_filter = get_frame_filter()
    wifi_frame = get_wifi_frame(0, 2)
    assert frame_filter.filter_frames_by_types(wifi_frame, [0])


def test_frame_filter_type_disallowed():
    frame_filter = get_frame_filter()
    wifi_frame = get_wifi_frame(1, 2)
    assert not frame_filter.filter_frames_by_types(wifi_frame, [0])


def test_frame_filter_type_none():
    frame_filter = get_frame_filter()
    wifi_frame = get_wifi_frame(None, 2)
    assert not frame_filter.filter_frames_by_types(wifi_frame, [0])


def test_filter_on_generator_allowed():
    frame_filter = get_frame_filter()
    wifi_frame = get_wifi_frame(0, 2)
    assert list(frame_filter.filter([wifi_frame]))[0] == wifi_frame


def test_filter_on_generator_disallowed():
    frame_filter = get_frame_filter()
    wifi_frame = get_wifi_frame(1, 2)
    assert len(list(frame_filter.filter([wifi_frame]))) == 0


def test_filter_on_generator_none():
    frame_filter = get_frame_filter()
    wifi_frame = get_wifi_frame(None, None)
    assert len(list(frame_filter.filter([wifi_frame]))) == 0


def test_filter_on_generator_mixed_multiple():
    frame_filter = get_frame_filter()
    wifi_frames = [
        get_wifi_frame(0, 2),
        get_wifi_frame(1, 2),
        get_wifi_frame(0, 3),
        get_wifi_frame(1, 3),
    ]

    result = list(frame_filter.filter(wifi_frames))

    assert len(result) == 2
    assert result[0] == wifi_frames[0]
    assert result[1] == wifi_frames[2]
