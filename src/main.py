from sympy import Point2D

from src.behaviour import Classifier
from src.config_loader import load_config_file
from src.pipeline_factory import PipelineFactory
from src.wifi.wifi_card import WifiCard

if __name__ == '__main__':
    config = load_config_file("config.yml")

    adapters = [WifiCard(name, Point2D(wifi_card['location'])) for name, wifi_card in config['adapters'].items()]

    PipelineFactory.input_wifi_listeners(adapters) \
        .filter(lambda frame: frame.frame_control_information.transmitter_address == "44:bb:3b:03:49:d6") \
        .add_frame_aggregator(threshold=len(adapters)) \
        .add_frame_to_device_converter() \
        .add_device_aggregator() \
        .add_average_rssi_with_variance() \
        .add_location_non_linear_least_square(do_draw=True) \
        .output_to_console() \
        .to_list()
