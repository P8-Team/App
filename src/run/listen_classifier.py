from sympy import Point2D

from src.classifier import Classifier
from src.config_loader import load_config_file
from src.pipeline_factory import PipelineFactory
from src.wifi.wifi_card import WifiCard

if __name__ == '__main__':
    config = load_config_file("config.yml")

    adapters = [WifiCard(name, Point2D(wifi_card['location'])) for name, wifi_card in config['adapters'].items()]

    cl = Classifier(config)
    cl.load_model('model_with_camera_labels')

    PipelineFactory.input_wifi_listeners(adapters) \
        .filter(lambda frame: frame.wlan_radio.signals[0].signal_strength is not None) \
        .add_frame_aggregator(threshold=len(adapters)) \
        .add_frame_to_device_converter() \
        .add_device_aggregator(config['device_buffer_size']) \
        .add_classifier(cl) \
        .add_average_rssi_with_variance() \
        .add_location_non_linear_least_square(config['path_loss_exponent'],
                                              config['transmission_power_placeholder_2ghz'],
                                              config['transmission_power_placeholder_5ghz'],
                                              do_draw=False) \
        .output_to_console() \
        .to_list()
