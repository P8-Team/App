from typing import List

import pytest
from sympy import Point2D

from src.classifier import Classifier
from src.data_generators.location_data_generator import LocationGenerator
from src.pipeline_factory import PipelineFactory
from src.wifi.frame_control_information import FrameControlInformation
from src.wifi.signal import Signal
from src.wifi.wifi_frame import WifiFrame
from src.wifi.wlan_radio_information import WlanRadioInformation
from test.utils.wifi_frame_factory import frame_factory

address_for_test_1 = "00:00:00:00:00:01"
address_for_test_2 = "00:00:00:00:00:02"
address_for_test_3 = "00:00:00:00:00:03"

position_precision = 0.5

transmission_power_2ghz = -15.5
transmission_power_5ghz = -10


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
        .add_location_non_linear_least_square(4, transmission_power_2ghz, transmission_power_5ghz)

    result = set(generator.to_list())

    assert len(result) == 1


def test_input_to_output_two_physical_addresses_two_devices_in_result(input_to_output_wifi_frames: List[WifiFrame]):
    generator = PipelineFactory(input_to_output_wifi_frames) \
        .add_type_subtype_filter(whitelisted_types=[1], whitelisted_subtypes=[1]) \
        .add_frame_aggregator(threshold=3) \
        .add_frame_to_device_converter() \
        .add_device_aggregator() \
        .add_average_rssi_with_variance() \
        .add_location_non_linear_least_square(4, transmission_power_2ghz, transmission_power_5ghz)

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
        .add_location_non_linear_least_square(4, transmission_power_2ghz, transmission_power_5ghz)

    result = generator.to_list()

    assert result[-1].position == pytest.approx([3, 3], position_precision)


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
        .add_location_non_linear_least_square(4, transmission_power_2ghz, transmission_power_5ghz)

    result = generator.to_list()

    assert result[-1].position == pytest.approx([3, 3], position_precision)


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
        .add_location_non_linear_least_square(4, transmission_power_2ghz, transmission_power_5ghz)

    result = generator.to_list()

    # Why doesn't this result in 3,3 because of average?
    # Because of weights: The point is much closer to the first anchor, and with much less variance.
    # Verified via do_draw=True
    assert result[-1].position == pytest.approx([-0.49722820384734406, 0.9675233314448546], position_precision)


def generate_tests_positions_and_check_for_failures(frame_generator: LocationGenerator,
                                                    precision=1.0, bounds=10):
    points = []
    wifi_frames = []
    number_of_positions = 0
    for x in range(-bounds, bounds + 1):
        for y in range(-bounds, bounds + 1):
            points.append([x, y])
            wifi_frames.append(
                frame_generator.make_wifi_element(Point2D([x, y]), transmitter_address=str(number_of_positions)))
            number_of_positions = number_of_positions + 1

    generator = PipelineFactory(wifi_frames) \
        .add_frame_to_device_converter() \
        .add_device_aggregator() \
        .add_average_rssi_with_variance() \
        .add_location_non_linear_least_square(4, transmission_power_2ghz, transmission_power_5ghz)

    result = generator.to_list()

    failures = 0
    for i in range(number_of_positions):
        if result[i].position != pytest.approx(points[i], abs=precision, rel=None):
            failures = failures + 1

            # calculate_position(result[i], do_draw=True)
            # print(result[i].position, points[i])

    # print(number_of_positions)

    return failures


def test_input_to_output_with_location_generator_large_distance_between_anchors_with_classifier():
    wifi_frame_generator = LocationGenerator([Point2D([0, 4.33]), Point2D([5, -4.33]), Point2D([-5, -4.33])],
                                             rounding=True)

    wifi_frames = [
        wifi_frame_generator.make_wifi_element(Point2D([3, 3]), transmission_power_dbm=-23, sniff_timestamp=1,
                                               receiver_address="0"),
        wifi_frame_generator.make_wifi_element(Point2D([3, 3]), transmission_power_dbm=-23, sniff_timestamp=2,
                                               receiver_address="1"),
        wifi_frame_generator.make_wifi_element(Point2D([3, 3]), transmission_power_dbm=-23, sniff_timestamp=100,
                                               receiver_address="2"),
    ]

    test_config = {'label_device_map': 'Data/label_device_maps/label_device_map.csv',
                   'classifier_interval': 1,
                   'confidence_threshold': 0.6,
                   'classifier_train_split': 0.25,
                   'address_label_map': 'Data/address_label_maps/address_label_map.csv',
                   'saved_models_folder': 'Data/cache/savedModels/',
                   'training_files': {'Google Nest': ['file1', 'file2', 'file3']},
                   'cache_folder': 'Data/cache/'}

    classifier = Classifier(test_config)
    classifier.load_model('test-trainedModel')

    generator = PipelineFactory(wifi_frames) \
        .add_frame_to_device_converter() \
        .add_device_aggregator() \
        .add_classifier(classifier) \
        .add_average_rssi_with_variance() \
        .add_location_non_linear_least_square(4, transmission_power_2ghz, transmission_power_5ghz, do_draw=False)

    result = generator.to_list()

    assert result[-1].position == pytest.approx([3, 3], position_precision)


@pytest.mark.slow
def test_input_to_output_fixed_positions_huge_distance_no_rounding_within_centimeter():
    wifi_frame_generator = LocationGenerator([Point2D([0, 43.3]), Point2D([50, -43.3]), Point2D([-50, -43.3])],
                                             rounding=False)

    assert generate_tests_positions_and_check_for_failures(wifi_frame_generator, precision=0.01) == 0


@pytest.mark.slow
def test_input_to_output_fixed_positions_large_distance_no_rounding_within_centimeter():
    wifi_frame_generator = LocationGenerator([Point2D([0, 4.33]), Point2D([5, -4.33]), Point2D([-5, -4.33])],
                                             rounding=False)

    assert generate_tests_positions_and_check_for_failures(wifi_frame_generator, precision=0.01) == 0


@pytest.mark.slow
def test_input_to_output_fixed_positions_small_distance_no_rounding_within_ten_meters():
    wifi_frame_generator = LocationGenerator([Point2D([0, 0.433]), Point2D([0.5, -0.433]), Point2D([-0.5, -0.433])],
                                             rounding=False)

    assert generate_tests_positions_and_check_for_failures(wifi_frame_generator, precision=10, bounds=5) == 0


@pytest.mark.slow
def test_input_to_output_fixed_positions_large_distance_with_rounding_within_two_meters():
    wifi_frame_generator = LocationGenerator([Point2D([0, 4.33]), Point2D([5, -4.33]), Point2D([-5, -4.33])],
                                             rounding=True)

    assert generate_tests_positions_and_check_for_failures(wifi_frame_generator, precision=2) == 0
