import os
from hashlib import sha1
from os.path import exists

import pandas as pd
from sympy import Point2D

from src.multiprocess_wifi_listener import cache_dataframe, load_cached_dataframe, map_to_frames
from src.wifi.wifi_card import WifiCard
from src.wifi.wifi_frame import WifiFrame
from test.utils.wifi_test_utils import Frame, Layer

frame1 = Frame("340", "1647417907.513663000", {
    'wlan': Layer({
        'fcs': '0x1234',
        'wlan.fc.type': '0',
        'wlan.fc.subtype': '4',
        'wlan.ra_resolved': '00:0c:29:b7:d9:b0',
        'wlan.ta_resolved': '00:0c:29:b7:d9:b1',
    }),
    'wlan_radio': Layer({
        'wlan_radio.signal_dbm': '-62',
        'wlan_radio.data_rate': '54',
        'wlan_radio.timestamp': '1567757308'
    })
})

frame2 = Frame("111", "1647417907.513663000", {
    'wlan': Layer({
        'fcs': '0x1235',
        'wlan.fc.type': '0',
        'wlan.fc.subtype': '4',
        'wlan.ra_resolved': '00:0c:29:b7:d9:b1',
        'wlan.ta_resolved': '7c:49:eb:40:22:2f',
    }),
    'wlan_radio': Layer({
        'wlan_radio.signal_dbm': '-62',
        'wlan_radio.data_rate': '54',
        'wlan_radio.timestamp': '1567757312'
    })
})


def test_map_to_frames():
    wifi_card = WifiCard("test", Point2D(0, 0))
    expected = [WifiFrame.from_frame(frame1, wifi_card), WifiFrame.from_frame(frame2, wifi_card)]
    result = map_to_frames([frame1, frame2], wifi_card)
    assert result == expected


def test_cache_dataframe():
    data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
    df = pd.DataFrame.from_dict(data)
    os.mkdir("cache")
    cache_dataframe("cache", "test", df)

    assert exists(f"cache/{sha1('test'.encode('utf-8')).hexdigest()}.json")
    os.remove(f"cache/{sha1('test'.encode('utf-8')).hexdigest()}.json")
    os.rmdir("cache")


def test_load_cached_dataframe():
    data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
    expected = pd.DataFrame.from_dict(data)
    os.mkdir("cache")
    cache_dataframe("cache", "test", expected)

    actual = load_cached_dataframe("cache", "test")

    pd.testing.assert_frame_equal(actual, expected)
    os.remove(f"cache/{sha1('test'.encode('utf-8')).hexdigest()}.json")
    os.rmdir("cache")
