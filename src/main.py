import argparse

from src.multiprocess_wifi_listener import sniff_filtered_combined_packages
from src.frame_filter import FrameFilter

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='P8 App - Wifi Sniffer')
    parser.add_argument('interfaces', nargs='+', help='Interfaces to sniff on')

    args = parser.parse_args()

    for frame in sniff_filtered_combined_packages(args.interfaces, FrameFilter(whitelisted_types=[0, 1, 2, 3, 4])):
        print(frame)
