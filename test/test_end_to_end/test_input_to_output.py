from typing import List
import pytest
from sympy import Point2D

from src.classifier import Classifier, Label
from src.pipeline_factory import PipelineFactory
from src.wifi.wifi_frame import WifiFrame
from test.utils.wifi_frame_factory import frame_factory


@pytest.fixture(autouse=True)
def wifi_frames():
    return [
        frame_factory(timestamp=0, location=Point2D([0, 1]), frame_control_sequence=1),
        frame_factory(timestamp=0.01, location=Point2D([1, 0]), frame_control_sequence=1),
        frame_factory(timestamp=0.02, location=Point2D([1, 1]), frame_control_sequence=1),
        frame_factory(timestamp=0.11, location=Point2D([0, 1]), frame_control_sequence=2),
        frame_factory(timestamp=0.12, location=Point2D([1, 0]), frame_control_sequence=2),
        frame_factory(timestamp=0.13, location=Point2D([1, 1]), frame_control_sequence=2),
        frame_factory(timestamp=0.23, location=Point2D([0, 1]), frame_control_sequence=3),
        frame_factory(timestamp=0.24, location=Point2D([1, 0]), frame_control_sequence=3),
        frame_factory(timestamp=0.24, location=Point2D([1, 1]), frame_control_sequence=3),
        frame_factory(timestamp=2.23, location=Point2D([0, 1]), frame_control_sequence=4),
        frame_factory(timestamp=2.23, location=Point2D([1, 0]), frame_control_sequence=4),
        frame_factory(timestamp=2.23, location=Point2D([1, 1]), frame_control_sequence=4),
    ]

def test_it_gets_location_in_combined_frames(wifi_frames: List[WifiFrame]):
    # get first 3 frames
    wifi_frames = wifi_frames[:3]

    # Then run the test
    generator = PipelineFactory(wifi_frames) \
        .add_type_subtype_filter(whitelisted_types=[1], whitelisted_subtypes=[1]) \
        .add_frame_aggregator(threshold=3) \
        .add_location_multilateration()

    result = generator.to_list()

    assert len(result) == 1
    assert result[0].location is not None
