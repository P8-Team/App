from hashlib import sha1
from multiprocessing import Queue, Process
from os.path import exists
from typing import Generator
from typing import Iterator

import pandas as pd
import pyshark
from pandas import DataFrame
from sympy import Point2D

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


def multiprocess_wifi_listener(wifi_card_list: list[WifiCard]) -> Iterator[WifiFrame]:
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
    if not exists(f'{cache_folder}/{sha1(file_path.encode("utf-8")).hexdigest()}.json'):
        print(f'No cached dataframe found for {file_path}. loading frames from file')
        frames = map_to_frames(load_file(file_path), WifiCard("file", Point2D(0, 0)))
        dfs = list()
        for item in frames:
            dfs.append(item.to_dataframe())
        df = pd.concat(dfs)
        print(f'Caching file {file_path}')
        cache_dataframe(cache_folder, file_path, df)
        return df
    else:
        print(f'Using cached dataframe for {file_path}')
        return load_cached_dataframe(cache_folder, file_path)


def load_file(file_path: str) -> list[WifiFrame]:
    if not exists(file_path):
        raise FileNotFoundError
    file = pyshark.FileCapture(file_path)
    result = list(file)
    file.close()
    return result


def map_to_frames(iterator, wifi_card):
    return list(map(lambda x: WifiFrame.from_frame(x, wifi_card), iterator))


def cache_dataframe(cache_folder: str, name: str, df: DataFrame) -> None:
    df.to_json(f"{cache_folder}/{sha1(name.encode('utf-8')).hexdigest()}.json", orient='records', default_handler=str)


def load_cached_dataframe(cache_folder: str, name: str) -> DataFrame:
    return pd.read_json(f"{cache_folder}/{sha1(name.encode('utf-8')).hexdigest()}.json", orient='records')
