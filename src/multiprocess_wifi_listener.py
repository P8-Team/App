from multiprocessing import Queue, Process

import pyshark

from src.frame_aggregator import frame_aggregator
from src.wifi_frame import WifiFrame


def wifi_listener(wifi_card_name, wifi_card, queue):
    """
        Starts a listener on a given Wi-Fi interface name
        This function does NOT handle putting the interface in monitor mode or setting the monitor frequency.

    :param wifi_card:
    :param queue:
    :return:
    """
    print("Starting listener on {}".format(wifi_card_name))

    for frame in pyshark.LiveCapture(interface=wifi_card_name, debug=True):
        queue.put(WifiFrame.from_frame(frame,wifi_card))


def multiprocess_wifi_listener(wifi_interface_list):
    """
        Starts a listener on each Wi-Fi interface name in the provided list and collects it into a single generator.
    :param wifi_interface_list:
    :return: generator of WifiFrames
    """
    queue = Queue()

    # Create a new process for each WiFi card
    print(wifi_interface_list)

    for wifi_card_name, wifi_card in wifi_interface_list.items():
        p = Process(target=wifi_listener, args=(wifi_card_name, wifi_card, queue))
        p.start()

    # Wait for queue entries and yield them
    while True:
        yield queue.get()

        # yield queue.get()
