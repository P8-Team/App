from multiprocessing import Queue, Process
from typing import Generator
from os.path import exists
from sympy import Point2D
import pandas as pd
from pandas import DataFrame

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

def frames_from_file_with_caching(file_path: str) -> Generator[WifiFrame, None, None]:
    cache_folder = "Data/cache"
    if not exists(f'{cache_folder}/{file_path}.json'):
        print('No cached file found. loading file')
        frames = frames_from_file(file_path)
        dfs = list()
        for item in frames:
            dfs.append(item.to_dataframe())
        df = pd.concat(dfs)
        print(f'Caching file {file_path}')
        cache_dataframe(cache_folder, file_path, df)
        return df
    else:
        return load_cached_dataframe(cache_folder, file_path)

def cache_dataframe(cache_folder: str, name: str, df: DataFrame) -> None:
    df.to_json(f"{cache_folder}/{name}.json", orient='records', default_handler=str)

def load_cached_dataframe(cache_folder: str, name:str) -> DataFrame:
    return pd.read_json(f"{cache_folder}/{name}.json", orient='records')

def frames_from_file(file_path: str) -> Generator[WifiFrame, None, None]:
    """
        Creates a generator that yields WifiFrames created from the given file
    :param file_name: Path to the file
    :return: Generator of WifiFrames
    """

    if not exists(file_path):
        raise FileNotFoundError
    print("Starting Listener on {}".format(file_path))
    wifi_card = WifiCard("file", Point2D(0, 0))

    file = pyshark.FileCapture(file_path)
    frames = list(file)
    print(f'file contains {len(frames)} frames')
    file.close()
    for frame in frames:
        yield WifiFrame.from_frame(frame, wifi_card)

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