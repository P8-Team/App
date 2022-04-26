import pytest
from sympy import Point2D

from src.location.multi_lateration_non_linear_least_square_sum import append_location_from_anchors_with_distance
from src.wifi.signal import Signal
from test.utils.wifi_frame_factory import frame_factory


def test_it_calculates_location():
    frame = frame_factory(0)

    # assign some signals
    frame.wlan_radio.signals = [
        Signal(Point2D(0,0), -20, 0, variance=1),
        Signal(Point2D(0,1), -22, 0, variance=1),
        Signal(Point2D(1,0), -23, 0, variance=1),
    ]

    # calculate the location
    res = append_location_from_anchors_with_distance(frame, do_draw=False)

    assert res.location == pytest.approx([0.8389631665687186, 0.7858192567441246])