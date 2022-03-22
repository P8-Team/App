print("Howdy folks!")

from src.multiprocess_wifi_listener import sniff_filtered_combined_packages
from src.packet_filter import PacketFilter

if __name__ == '__main__':
    for packet in sniff_filtered_combined_packages(["Wi-Fi"], PacketFilter(whitelisted_types=[0, 1, 2, 3, 4])):
        print(packet)
