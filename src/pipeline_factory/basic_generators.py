import csv
import io
import json
from typing import Iterator

import pyshark

from src.location.distance_strength_calculations import signal_strength_dbm_to_distance
from src.location.simple_location import location
from src.wifi.wifi_frame import WifiFrame


def json_generator(generator):
    for item in generator:
        yield json.dumps(item, default=vars)


def output_to_console_generator(generator):
    for item in generator:
        print(item)
        yield item


def output_to_file_generator(generator, file_path, mode='a', encoding='utf-8', newline='\n'):
    for item in generator:
        with open(file_path, mode, encoding=encoding, newline=newline) as f:
            f.write(item)
            f.write(newline)
        yield item


def csv_row_generator(generator, delimiter=';'):
    for item in generator:
        output = io.StringIO()
        csv.writer(output, delimiter=delimiter).writerow(item)
        yield output.getvalue()


def pcap_file_generator(file_path):
    return pyshark.FileCapture(file_path)


def filter(generator: Iterator[WifiFrame], filter_function):
    for item in generator:
        if filter_function(item):
            yield item


def apply(generator: Iterator[WifiFrame], function):
    for item in generator:
        yield function(item)


def csv_reader(filename, skip_header):
    with open(filename, 'r') as csv_file:
        if skip_header:
            next(csv_file)
        for line in csv_file:
            yield WifiFrame.from_csv_row(line)


def append_location_to_wifi_frame(generator: Iterator[WifiFrame]) -> Iterator[WifiFrame]:
    for item in generator:
        print(item.wlan_radio.__dict__)
        wifi_interface_with_distance = [
            [
                signal.location.x,
                signal.location.y,
                signal_strength_dbm_to_distance(20 if item.wlan_radio.frequency_mhz < 4000 else 30,
                                                signal.signal_strength, item.wlan_radio.frequency_mhz)
            ] for signal in item.wlan_radio.signals]
        item.location = location(wifi_interface_with_distance)
        yield item
