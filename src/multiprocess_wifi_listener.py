from multiprocessing import Queue, Process

import pyshark

from src.frame_aggregator import frame_aggregator
from src.packet_filter import PacketFilter
from src.wifi_frame import WifiFrame


def wifi_listener(wifi_card, queue):
    """
        Starts a listener on a given Wi-Fi interface name
        This function does NOT handle putting the interface in monitor mode or setting the monitor frequency.

    :param wifi_card:
    :param queue:
    :return:
    """
    for frame in pyshark.LiveCapture(interface=wifi_card, monitor_mode=True):
        queue.put(WifiFrame.from_frame(frame))


def multiprocess_wifi_listener(wifi_interface_list):
    """
        Starts a listener on each Wi-Fi interface name in the provided list and collects it into a single generator.
    :param wifi_interface_list:
    :return: generator of WifiFrames
    """
    queue = Queue()

    # Create a new process for each WiFi card
    for wifi_card in wifi_interface_list:
        p = Process(target=wifi_listener, args=(wifi_card, queue))
        p.start()

    # Wait for queue entries and yield them
    while True:
        yield queue.get()


def sniff_filtered_combined_packages(wifi_interface_list, packet_filter):
    """
        Starts a listener on each Wi-Fi interface name in the provided list and collects it into a single generator.
        The generator is filtered by the provided PacketFilter and frames are combined.
    :param packet_filter:
    :param wifi_interface_list:
    :return:
    """
    for frame in frame_aggregator(
            packet_filter.filter(multiprocess_wifi_listener(wifi_interface_list)),
            threshold=len(wifi_interface_list)
    ):
        yield frame
