import pyshark

from src.filter_raw_frames import FilterFrameIterator
from src.wifi_frame import WifiFrame

if __name__ == '__main__':
    capture = pyshark.LiveCapture(interface='Wi-Fi', monitor_mode=True)
    capture.set_debug()

    for packet in FilterFrameIterator().filter_raw_frames(capture):
        print(WifiFrame(packet))
        break

