from sympy import Point2D

from src.config_loader import load_config_file
from src.device.device import Device
from src.oracle import Oracle
from src.pipeline_factory import PipelineFactory
from src.wifi.wifi_card import WifiCard


def run_pipeline(file_name, devices_tested, distance, device_address, label,
                 adapters: list[WifiCard], config, oracle, weighted=True):
    output_file_name = f"result_distance_{distance}_devices_{devices_tested}_" \
                       f"path_{config['path_loss_exponent']}_{label}_{'weighted' if weighted else 'unweighted'}.csv"
    print(f"Output file name: {output_file_name}")
    with open(output_file_name, 'w') as f:
        f.write(Device.get_csv_header())

    PipelineFactory.from_csv_file(file_name, skip_header=False) \
        .filter(lambda frame: frame.frame_control_information.transmitter_address == device_address) \
        .filter(lambda frame: frame.wlan_radio.signals[0].signal_strength is not None) \
        .filter(lambda frame: frame.frame_control_information.transmitter_address in device_address_dict) \
        .add_frame_aggregator_sniff_timestamp(threshold=len(adapters)) \
        .add_frame_to_device_converter() \
        .add_device_aggregator(config['device_buffer_size']) \
        .add_oracle(oracle) \
        .add_average_rssi_with_variance() \
        .add_location_non_linear_least_square(config['path_loss_exponent'],
                                              config['transmission_power_placeholder_2ghz'],
                                              config['transmission_power_placeholder_5ghz'],
                                              do_draw=False) \
        .apply(lambda device: device.to_csv_row()) \
        .output_to_file(output_file_name) \
        .to_list()


if __name__ == '__main__':
    config = load_config_file("config.yml")

    adapters = [WifiCard(name, Point2D(wifi_card['location'])) for name, wifi_card in config['adapters'].items()]

    device_address_dict = {
        "50:8a:06:3f:27:9b": [-23, "LittleElf"],
        "dc:29:19:94:b1:f8": [-23, "Nikkei"],
        "48:78:5e:bd:a9:44": [-7, "Blink"],
    }
    oracle = Oracle(device_address_dict)

    files_all = {
        "experiments/experiment_10_3.csv": 10,
        "experiments/experiment_5_3.csv": 5,
        "experiments/experiment_1_3.csv": 1
    }

    # loop files_all
    for file_name, distance in files_all.items():
        for device_address, label in device_address_dict.items():
            run_pipeline(file_name, 3, distance, device_address, label[1], adapters, config, oracle, weighted=True)
            run_pipeline(file_name, 3, distance, device_address, label[1], adapters, config, oracle, weighted=False)

    files_single = {
        "experiments/experiment_10_1.csv": 10,
        "experiments/experiment_5_1.csv": 5,
        "experiments/experiment_1_1.csv": 1
    }

    # loop files_single
    for file_name, distance in files_single.items():
        run_pipeline(file_name, 1, distance, "dc:29:19:94:b1:f8", "Nikkei", adapters, config, oracle, weighted=True)
        run_pipeline(file_name, 1, distance, "dc:29:19:94:b1:f8", "Nikkei", adapters, config, oracle, weighted=False)
