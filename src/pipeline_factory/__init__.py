from src.frame_aggregator import frame_aggregator
from src.frame_filter import FrameFilter
from src.multiprocess_wifi_listener import multiprocess_wifi_listener
from src.pipeline_factory.basic_generators import csv_row_generator, output_to_file_generator, \
    output_to_console_generator


class PipelineFactory:

    def __init__(self, generator):
        self.generator = generator

    @classmethod
    def input_wifi_listeners(cls, wlan_interfaces):
        return cls(multiprocess_wifi_listener(wlan_interfaces))

    def add_type_subtype_filter(self, whitelisted_types=None, whitelisted_subtypes=None):
        frame_filter = FrameFilter(whitelisted_types, whitelisted_subtypes)
        self.generator = FrameFilter.filter(self.generator, frame_filter)
        return self

    def add_frame_aggregator(self, threshold=None, max_age_seconds=None, max_buffer_size=None):
        self.generator = frame_aggregator(self.generator, threshold, max_age_seconds, max_buffer_size)
        return self

    def add_location_multilateration(self):
        return self

    def add_basic_classifier(self):
        return self

    def output_to_console(self):
        self.generator = output_to_console_generator(self.generator)
        return self

    def transform_to_json(self):
        self.generator = json_generator(self.generator)

    def output_to_file(self, filename):
        self.generator = output_to_file_generator(self.generator, filename)
        return self

    def transform_to_csv_row(self, delimiter=';'):
        self.generator = csv_row_generator(self.generator, delimiter)
        return self
