from __future__ import annotations

from src.frame_aggregator import frame_aggregator
from src.frame_filter import FrameFilter
from src.multiprocess_wifi_listener import multiprocess_wifi_listener
from src.pipeline_factory.basic_generators import csv_row_generator, output_to_file_generator, \
    output_to_console_generator, json_generator, pcap_file_generator, append_location_to_wifi_frame
from src.wifi.wifi_card import WifiCard


class PipelineFactory:

    def __init__(self, generator):
        self.generator = generator

    @classmethod
    def input_wifi_listeners(cls, wlan_interfaces: list[WifiCard]) -> PipelineFactory:
        return cls(multiprocess_wifi_listener(wlan_interfaces))

    @classmethod
    def input_pcap_file(cls, filename):
        return cls(pcap_file_generator(filename))

    def add_type_subtype_filter(self, whitelisted_types=None, whitelisted_subtypes=None):
        frame_filter = FrameFilter(whitelisted_types, whitelisted_subtypes)
        self.generator = frame_filter.filter(self.generator)
        return self

    def add_frame_aggregator(self, threshold=None, max_age_seconds=None, max_buffer_size=None):
        self.generator = frame_aggregator(self.generator, threshold, max_age_seconds, max_buffer_size)
        return self

    def add_location_multilateration(self):
        self.generator = append_location_to_wifi_frame(self.generator)
        return self

    def add_classifier(self, classifier):
        self.generator = classifier.classify(self.generator)
        return self

    def output_to_console(self):
        self.generator = output_to_console_generator(self.generator)
        return self

    def transform_to_json(self):
        self.generator = json_generator(self.generator)
        return self

    def output_to_file(self, filename):
        self.generator = output_to_file_generator(self.generator, filename)
        return self

    def transform_to_csv_row(self, delimiter=';'):
        self.generator = csv_row_generator(self.generator, delimiter)
        return self

    def to_list(self):
        return list(self.generator)
