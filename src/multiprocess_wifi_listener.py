from multiprocessing import Queue, Process
from typing import Generator

import pyshark

from src.wifi.wifi_card import WifiCard
from src.wifi.wifi_frame import WifiFrame


def wifi_listener(wifi_card: WifiCard, queue: Queue) -> None:
    """
        Starts a listener on a given Wi-Fi interface name
        This function does NOT handle putting the interface in monitor mode or setting the monitor frequency.

    :param wifi_card:
    :param queue:
    :return:
    """
    print("Starting listener on {}".format(wifi_card.interface_name))

    for frame in pyshark.LiveCapture(interface=wifi_card.interface_name, debug=True):
        queue.put(WifiFrame.from_frame(frame, wifi_card))


def multiprocess_wifi_listener(wifi_card_list: list[WifiCard]) -> Generator[WifiFrame, None, None]:
    """
        Starts a listener on each Wi-Fi interface name in the provided list and collects it into a single generator.
    :param wifi_card_list:
    :return: generator of WifiFrames
    """
    queue = Queue()

    # Create a new process for each WiFi card
    print(wifi_card_list)

    for wifi_card in wifi_card_list:
        p = Process(target=wifi_listener, args=(wifi_card, queue))
        p.start()

    # Wait for queue entries and yield them
    while True:
        yield queue.get()
