import argparse

from src.config_loader import load_config
from src.multiprocess_wifi_listener import sniff_filtered_combined_packages
from src.frame_filter import FrameFilter
from src.pipeline_factory import PipelineFactory

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='P8 App - Wifi Sniffer')
    parser.add_argument('interfaces', nargs='+', help='Interfaces to sniff on')

    config = load_config("config.yml")
    print(config)

    args = parser.parse_args()

    generator = PipelineFactory.input_wifi_listeners(config['adapters'])\
        .add_type_subtype_filter()\
        .add_frame_aggregator()\
        .add_location_multilateration()\
        .add_basic_classifier()\
        .output_to_console()\
        .output_to_file()\

    for frame in sniff_filtered_combined_packages(args.interfaces, FrameFilter(whitelisted_types=[0, 1, 2, 3, 4])):
        print(frame)
