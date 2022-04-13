import csv
import io
import json
from typing import Generator

import pyshark

from src.distance_strength_calculations import calc_distance_from_dbm_signal_strength
from src.location import location
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

def append_location_to_wifi_frame(generator: Generator[WifiFrame, None, None]) -> Generator[WifiFrame, None, None]:
    for item in generator:
        print(item.wlan_radio.__dict__)
        wifi_interface_with_distance = [
            [
                signal.location.x,
                signal.location.y,
                calc_distance_from_dbm_signal_strength(20 if item.wlan_radio.frequency_mhz < 4000 else 30, signal.signal_strength, item.wlan_radio.frequency_mhz)
            ] for signal in item.wlan_radio.signals]
        item.location = location(wifi_interface_with_distance)
        yield item


