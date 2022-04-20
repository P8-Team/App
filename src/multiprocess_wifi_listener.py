from multiprocessing import Queue, Process
from typing import Generator
from os.path import exists
from sympy import Point2D

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

def wifi_listener_from_file(file_name: str, queue: Queue):
    """
        Starts a listener on a given file.
    :param file_name: File path to the file
    :param queue:
    :return:
    """

    if not exists(file_name):
        raise FileNotFoundError
    print("Starting Listener on {}".format(file_name))
    wifi_card = WifiCard("file", Point2D(0, 0))

    file = pyshark.FileCapture(file_name)
    for frame in file:
        queue.put(WifiFrame.from_frame(frame, wifi_card))
    file.close()

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
