from multiprocessing import Queue
import pandas as pd
import json
from os.path import exists
import os
from hashlib import sha1


import pytest

from src.multiprocess_wifi_listener import frames_from_file, cache_dataframe, load_cached_dataframe

def test_wifi_frames_from_file_given_nonexistent_file():
    filepath = "NOT A VALID FILE PATH"
    with pytest.raises(FileNotFoundError):
        next(frames_from_file(filepath))

def test_wifi_frames_from_file_given_existing_file():
    filepath = "test/test_data/dump.pcapng"
    gen = frames_from_file(filepath)
    first_element = next(gen)
    assert first_element.frame_control_information.transmitter_address == "7c:49:eb:40:22:2f"

def test_cache_dataframe():
    data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
    df = pd.DataFrame.from_dict(data)
    cache_dataframe("test/test_data/cache", "test", df)

    assert exists(f"test/test_data/cache/{sha1('test'.encode('utf-8')).hexdigest()}.json")
    os.remove(f"test/test_data/cache/{sha1('test'.encode('utf-8')).hexdigest()}.json")

def test_load_cached_dataframe():
    data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
    expected = pd.DataFrame.from_dict(data)
    cache_dataframe("test/test_data/cache", "test", expected)

    actual = load_cached_dataframe("test/test_data/cache", "test")

    pd.testing.assert_frame_equal(actual, expected)
    os.remove(f"test/test_data/cache/{sha1('test'.encode('utf-8')).hexdigest()}.json")