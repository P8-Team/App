import pyshark

from src.packet_filter import PacketFilter
from src.wifi_frame import WifiFrame

if __name__ == '__main__':
    # Only used for debugging/manual testing purposes for now
    capture = pyshark.FileCapture(input_file="../wifi_data")
    # capture = pyshark.LiveCapture(interface='Wi-Fi', monitor_mode=True)
    capture.set_debug()

    for packet in PacketFilter().filter(WifiFrame.construct_from_iterator(capture)):
        print(packet)

