from sympy import Point2D

from src.config_loader import load_config_file
from src.oracle import Oracle
from src.pipeline_factory import PipelineFactory
from src.wifi.wifi_card import WifiCard

if __name__ == '__main__':
    config = load_config_file("config.yml")

    adapters = [WifiCard(name, Point2D(wifi_card['location'])) for name, wifi_card in config['adapters'].items()]

    device_address_dict = {
        "50:8a:06:3f:27:9b": [-23, "LittleElf"],
        "6c:5a:b0:42:02:58": [-6, "TP-Link"],
        "dc:29:19:94:b1:f8": [-23, "Nikkei"],
        "48:78:5e:bd:a9:44": [-7, "Blink"],
        "38:01:46:1d:bd:ec": [-17, "Nedis"]
    }

    oracle = Oracle(device_address_dict)

    # PipelineFactory.from_csv_file("experiments/experiment_1_3.csv", skip_header=False) \
    PipelineFactory.input_wifi_listeners(adapters) \
        .filter(lambda frame: frame.wlan_radio.signals[0].signal_strength is not None) \
        .add_frame_aggregator_sniff_timestamp(threshold=len(adapters)) \
        .add_frame_to_device_converter() \
        .add_device_aggregator(config['device_buffer_size']) \
        .add_oracle(oracle) \
        .add_average_rssi_with_variance() \
        .add_location_non_linear_least_square(config['path_loss_exponent'],
                                              config['transmission_power_placeholder_2ghz'],
                                              config['transmission_power_placeholder_5ghz'],
                                              do_draw=False) \
        .output_to_console() \
        .to_list()
