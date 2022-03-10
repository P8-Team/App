
# do pyshark stuff
import json

import pyshark

if __name__ == '__main__':
    # capture packets
    # monitor mode
    capture = pyshark.LiveCapture(interface='Wi-Fi', monitor_mode=True)
    capture.set_debug()
    for packet in capture:
        print("=====================================================")
        print("=====================================================")
        print("=====================================================")
        print(packet)
        # serialize packets content to json

        print(json.dumps(packet, indent=4))
        break

