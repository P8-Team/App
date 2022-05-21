from sympy import Point2D

from src.classifier import Classifier
from src.config_loader import load_config_file
from src.pipeline_factory import PipelineFactory
from src.wifi.wifi_card import WifiCard


def classification_output_runner(filename):
    print("Running function")
    config = load_config_file("config.yml")
    cl = Classifier(config)
    cl.load_model('model_with_camera_labels')
    adapters = [WifiCard(name, Point2D(wifi_card['location'])) for name, wifi_card in config['adapters'].items()]
    device_address_dict = {
        "50:8a:06:3f:27:9b": [-23, "LittleElf"],
        "dc:29:19:94:b1:f8": [-23, "Nikkei"],
        "48:78:5e:bd:a9:44": [-7, "Blink"],
    }

    PipelineFactory.from_csv_file(filename, skip_header=False) \
        .filter(lambda frame: frame.wlan_radio.signals[0].signal_strength is not None) \
        .filter(lambda frame: frame.frame_control_information.transmitter_address in device_address_dict) \
        .add_frame_aggregator_sniff_timestamp(threshold=len(adapters)) \
        .add_frame_to_device_converter() \
        .add_device_aggregator(config['device_buffer_size']) \
        .add_classifier(cl) \
        .apply(lambda device: device.to_csv_row()) \
        .output_to_file("output_file") \
        .to_list()


if __name__ == '__main__':
    path = "Data/experiments/"
    files = ["experiments_1_1.csv", "experiments_1_3.csv", "experiments_5_1.csv", "experiments_5_3.csv",
             "experiments_10_1.csv","experiments_10_3.csv"]
    for file in files:
        classification_output_runner(path + file)
