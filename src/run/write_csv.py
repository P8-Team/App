from sympy import Point2D
from src.config_loader import load_config_file
from src.pipeline_factory import PipelineFactory
from src.wifi.wifi_card import WifiCard

if __name__ == '__main__':
    config = load_config_file("config.yml")

    adapters = [WifiCard(name, Point2D(wifi_card['location'])) for name, wifi_card in config['adapters'].items()]

    PipelineFactory.input_wifi_listeners(adapters) \
        .apply(lambda wifi_frame: wifi_frame.to_csv_row()) \
        .output_to_console() \
        .output_to_file("test.csv") \
        .to_list()
