import argparse

from src.behaviour import Classifier
from src.config_loader import load_config_file
from src.frame_filter import FrameFilter
from src.pipeline_factory import PipelineFactory

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='P8 App - Wifi Sniffer')
    parser.add_argument('interfaces', nargs='+', help='Interfaces to sniff on')

    config = load_config_file("config.yml")
    print(config)

    args = parser.parse_args()

    generator = PipelineFactory.input_wifi_listeners(config['adapters'])\
        .add_frame_aggregator(threshold=1)\
        .add_location_multilateration()\
        .add_classifier(Classifier(1))\
        .output_to_console()\
        .transform_to_json()\
        .output_to_file("watafaka.wat")\
        .listen()

    #
    #     .add_type_subtype_filter()\

    # for frame in sniff_filtered_combined_packages(args.interfaces, FrameFilter(whitelisted_types=[0, 1, 2, 3, 4])):
    #     print(frame)
