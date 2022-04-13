from sympy import Point2D

from src.behaviour import Classifier
from src.config_loader import load_config_file
from src.pipeline_factory import PipelineFactory
from src.wifi.wifi_card import WifiCard

if __name__ == '__main__':
    config = load_config_file("config.yml")

    adapters = [WifiCard(name, Point2D(wifi_card['location'])) for name, wifi_card in config['adapters'].items()]

    generator = PipelineFactory.input_wifi_listeners(adapters)\
        .add_frame_aggregator(threshold=len(adapters))\
        .use_average_rssi_with_variance()\
        .add_location_non_linear_least_square()\
        .add_location_multilateration()\
        .add_classifier(Classifier(1))\
        .output_to_console()\
        .transform_to_json()\
        .output_to_file("out.json")\
        .to_list()
