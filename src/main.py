import pyshark

from src.wifi_frame import WifiFrame

if __name__ == '__main__':
    # Only used for testing purposes for now
    capture = pyshark.LiveCapture(interface='Wi-Fi', monitor_mode=True)
    capture.set_debug()

    for packet in capture:
        print(WifiFrame.from_frame(packet))
        break

