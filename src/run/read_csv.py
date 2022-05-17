from sympy import Point2D

from src.classifier import Classifier
from src.config_loader import load_config_file
from src.pipeline_factory import PipelineFactory
from src.wifi.wifi_card import WifiCard


if __name__ == '__main__':
    config = load_config_file("config.yml")

    adapters = [WifiCard(name, Point2D(wifi_card['location'])) for name, wifi_card in config['adapters'].items()]

    cl = Classifier(3)
    cl.load_model('test-trainedModel')

    PipelineFactory.from_csv_file("test.csv", skip_header=False) \
        .add_frame_aggregator(threshold=len(adapters)) \
        .add_frame_to_device_converter() \
        .add_device_aggregator() \
        .add_classifier(cl) \
        .add_average_rssi_with_variance() \
        .add_location_non_linear_least_square(3, do_draw=False) \
        .output_to_console() \
        .to_list()
