from sympy import Point2D

from src.config_loader import load_config_file
from src.oracle import Oracle
from src.pipeline_factory import PipelineFactory
from src.wifi.wifi_card import WifiCard
from src.data_generators.location_data_generator import LocationGenerator

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

    wifi_frame_generator = LocationGenerator([adapters[0].location, adapters[1].location, adapters[2].location])

    wifi_frames = [
        wifi_frame_generator.make_wifi_element(Point2D([5, 5]),
                                               sniff_timestamp=0, transmission_power_dbm=-23),
        wifi_frame_generator.make_wifi_element(Point2D([5, 5]),
                                               transmitter_address="50:8a:06:3f:27:9b",
                                               sniff_timestamp=1, transmission_power_dbm=-23),
    ]

    PipelineFactory(wifi_frames) \
        .add_frame_to_device_converter() \
        .add_device_aggregator(config['device_buffer_size']) \
        .add_oracle(oracle) \
        .add_average_rssi_with_variance() \
        .add_location_non_linear_least_square(config['path_loss_exponent'],
                                              config['transmission_power_placeholder_2ghz'],
                                              config['transmission_power_placeholder_5ghz'],
                                              do_draw=True) \
        .output_to_console() \
        .to_list()
