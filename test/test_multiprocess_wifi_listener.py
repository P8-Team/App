from multiprocessing import Queue

import pytest

from src.multiprocess_wifi_listener import wifi_listener_from_file


def test_multiprocess_wifi_listener_file_exists():
    queue = Queue()
    filepath = "test/test_data/dump.pcapng"
    wifi_listener_from_file(filepath,queue)
    first_element = queue.get()
    assert first_element.frame_control_information.transmitter_address == "7c:49:eb:40:22:2f"


def test_multiprocess_wifi_listener_file_not_exists():
    queue = Queue()
    filepath = "NOT A VALID FILE PATH"
    with pytest.raises(FileNotFoundError):
        wifi_listener_from_file(filepath,queue)
