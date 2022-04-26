from typing import List
import pytest
from sympy import Point2D

from src.behaviour import Classifier, Label
from src.pipeline_factory import PipelineFactory
from src.wifi.wifi_frame import WifiFrame
from test.utils.wifi_frame_factory import frame_factory
from src.wifi.wlan_radio_information import WlanRadioInformation
from src.wifi.frame_control_information import FrameControlInformation
from src.wifi.signal import Signal
from src.data_generators.location_data_generator import LocationGenerator

address_for_test_1 = "00:00:00:00:00:01"
address_for_test_2 = "00:00:00:00:00:02"
address_for_test_3 = "00:00:00:00:00:03"


@pytest.fixture(autouse=True)
def input_to_output_wifi_frames():
    return [
        wifi_frame(0.00, 100, Point2D([0, 0]), -40, address_for_test_1, address_for_test_2, 1),
        wifi_frame(0.01, 100, Point2D([0, 1]), -39, address_for_test_1, address_for_test_2, 1),
        wifi_frame(0.02, 100, Point2D([1, 0]), -38, address_for_test_1, address_for_test_2, 1),
        wifi_frame(0.10, 100, Point2D([0, 0]), -50, address_for_test_2, address_for_test_3, 2),
        wifi_frame(0.11, 100, Point2D([0, 1]), -49, address_for_test_2, address_for_test_3, 2),
        wifi_frame(0.12, 100, Point2D([1, 0]), -48, address_for_test_2, address_for_test_3, 2),
        wifi_frame(1.20, 100, Point2D([0, 0]), -30, address_for_test_1, address_for_test_3, 3),
        wifi_frame(1.21, 100, Point2D([0, 1]), -29, address_for_test_1, address_for_test_3, 3),
        wifi_frame(1.22, 100, Point2D([1, 0]), -28, address_for_test_1, address_for_test_3, 3),
        wifi_frame(2.10, 100, Point2D([0, 0]), -60, address_for_test_2, address_for_test_3, 4),
        wifi_frame(2.11, 100, Point2D([0, 1]), -59, address_for_test_2, address_for_test_3, 4),
        wifi_frame(2.12, 100, Point2D([1, 0]), -58, address_for_test_2, address_for_test_3, 4),
    ]


def wifi_frame(timestamp, length, location, signal_strength, transmitter_address, receiver_address,
               frame_control_sequence):
    return WifiFrame(length, frame_control_sequence,
                     WlanRadioInformation(
                         signals=[Signal(location, signal_strength, timestamp)],
                         frequency_mhz=2412
                     ),
                     FrameControlInformation(
                         transmitter_address=transmitter_address,
                         receiver_address=receiver_address,
                         fc_type=1,
                         subtype=1
                     ))


@pytest.fixture(autouse=True)
def wifi_frames():
    return [
        frame_factory(timestamp=0.00, location=Point2D([0, 1]), frame_control_sequence=1),
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


def test_it_classifies_wifi_frames_as_undesired(wifi_frames: List[WifiFrame]):
    # Then run the test
    generator = PipelineFactory(wifi_frames) \
        .add_type_subtype_filter(whitelisted_types=[1], whitelisted_subtypes=[1]) \
        .add_frame_aggregator(threshold=3) \
        .add_location_multilateration() \
        .add_classifier(Classifier(1))

    # convert generator to list
    result = generator.to_list()

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
        .output_to_console() \
        .add_classifier(Classifier(1))

    # convert generator to list
    result = generator.to_list()

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

    result = generator.to_list()

    assert len(result) == 1
    assert result[0].location is not None


def test_input_to_output_one_physical_address_one_device_in_result(wifi_frames: List[WifiFrame]):
    generator = PipelineFactory(wifi_frames) \
        .add_type_subtype_filter(whitelisted_types=[1], whitelisted_subtypes=[1]) \
        .add_frame_aggregator(threshold=3) \
        .add_frame_to_device_converter() \
        .add_device_aggregator() \
        .add_average_rssi_with_variance() \
        .add_location_non_linear_least_square()

    result = set(generator.to_list())

    assert len(result) == 1


def test_input_to_output_two_physical_addresses_two_devices_in_result(input_to_output_wifi_frames: List[WifiFrame]):
    generator = PipelineFactory(input_to_output_wifi_frames) \
        .add_type_subtype_filter(whitelisted_types=[1], whitelisted_subtypes=[1]) \
        .add_frame_aggregator(threshold=3) \
        .add_frame_to_device_converter() \
        .add_device_aggregator() \
        .add_average_rssi_with_variance() \
        .add_location_non_linear_least_square(do_draw=False)

    result = set(generator.to_list())

    assert len(result) == 2


def test_input_to_output_with_location_generator_small_distance_between_anchors():
    wifi_frame_generator = LocationGenerator([Point2D([0, 0.433]), Point2D([0.5, -0.433]), Point2D([-0.5, -0.433])])

    wifi_frames = [
        wifi_frame_generator.make_wifi_element(Point2D([3, 3])),
        wifi_frame_generator.make_wifi_element(Point2D([3, 3]))
    ]

    generator = PipelineFactory(wifi_frames) \
        .add_frame_to_device_converter() \
        .add_device_aggregator() \
        .add_average_rssi_with_variance() \
        .add_location_non_linear_least_square(do_draw=False)

    result = generator.to_list()

    assert result[-1].position == pytest.approx([3, 3], 0.5)


def test_input_to_output_with_location_generator_large_distance_between_anchors():
    wifi_frame_generator = LocationGenerator([Point2D([0, 4.33]), Point2D([5, -4.33]), Point2D([-5, -4.33])])

    wifi_frames = [
        wifi_frame_generator.make_wifi_element(Point2D([3, 3])),
        wifi_frame_generator.make_wifi_element(Point2D([3, 3]))
    ]

    generator = PipelineFactory(wifi_frames) \
        .add_frame_to_device_converter() \
        .add_device_aggregator() \
        .add_average_rssi_with_variance() \
        .add_location_non_linear_least_square(do_draw=False)

    result = generator.to_list()

    assert result[-1].position == pytest.approx([3, 3], 0.5)


def test_input_to_output_device_changes_position():
    wifi_frame_generator = LocationGenerator([Point2D([0, 4.33]), Point2D([5, -4.33]), Point2D([-5, -4.33])])

    wifi_frames = [
        wifi_frame_generator.make_wifi_element(Point2D([2, 2])),
        wifi_frame_generator.make_wifi_element(Point2D([4, 4]))
    ]

    generator = PipelineFactory(wifi_frames) \
        .add_frame_to_device_converter() \
        .add_device_aggregator() \
        .add_average_rssi_with_variance() \
        .add_location_non_linear_least_square(do_draw=False)

    result = generator.to_list()

    assert result[-1].position == pytest.approx([3, 3], 0.5)

