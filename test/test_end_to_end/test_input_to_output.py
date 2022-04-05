from typing import List
import pytest
from src.behaviour import Classifier, Label
from src.pipeline_factory import PipelineFactory
from src.wifi_frame import WifiFrame
from test.utils.wifi_frame_factory import frame_factory


@pytest.fixture(autouse=True)
def wifi_frames():
    return [
        frame_factory(timestamp=0, location=[0, 1]),
        frame_factory(timestamp=0.01, location=[1, 0]),
        frame_factory(timestamp=0.02, location=[1, 1]),
        frame_factory(timestamp=0.11, location=[0, 1]),
        frame_factory(timestamp=0.12, location=[1, 0]),
        frame_factory(timestamp=0.13, location=[1, 1]),
        frame_factory(timestamp=0.23, location=[0, 1]),
        frame_factory(timestamp=0.24, location=[1, 0]),
        frame_factory(timestamp=0.24, location=[1, 1]),
        frame_factory(timestamp=2.23, location=[0, 1]),
        frame_factory(timestamp=2.23, location=[1, 0]),
        frame_factory(timestamp=2.23, location=[1, 1]),
    ]


def test_it_classifies_wifi_frames_as_undesired(wifi_frames: List[WifiFrame]):
    # Then run the test
    generator = PipelineFactory(wifi_frames) \
        .add_type_subtype_filter(whitelisted_types=[1], whitelisted_subtypes=[1]) \
        .add_frame_aggregator(threshold=3) \
        .add_location_multilateration() \
        .add_classifier(Classifier(1))

    # convert generator to list
    result = list(generator.generator)

    assert len(result) == 1
    assert result[0] == Label.Undesired


def test_it_classifies_wifi_frames_as_desired(wifi_frames: List[WifiFrame]):
    # remove first 3 frames from wifi_frames
    wifi_frames = wifi_frames[3:]
    # Then run the test
    generator = PipelineFactory(wifi_frames) \
        .add_type_subtype_filter(whitelisted_types=[1], whitelisted_subtypes=[1]) \
        .add_frame_aggregator(threshold=3) \
        .add_location_multilateration() \
        .add_classifier(Classifier(1))

    # convert generator to list
    result = list(generator.generator)

    assert len(result) == 1
    assert result[0] == Label.Ok


def test_it_gets_location_in_combined_frames(wifi_frames: List[WifiFrame]):
    # get first 3 frames
    wifi_frames = wifi_frames[:3]

    # Then run the test
    generator = PipelineFactory(wifi_frames) \
        .add_type_subtype_filter(whitelisted_types=[1], whitelisted_subtypes=[1]) \
        .add_frame_aggregator(threshold=3) \
        .add_location_multilateration()

    result = list(generator.generator)

    assert len(result) == 1
    assert result[0].location is not None
