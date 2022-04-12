import pytest
from src.channel_hopper import ChannelHopper
import time


@pytest.mark.skip(reason="The result of the channel hopper can only be seen by "
                         "running 'sudo iwlist <interface> channel' and by looking at the console")
def test_channel_hopper_using_start():
    channel_hopper = ChannelHopper(["wlan4"])
    channel_hopper.start()
    time.sleep(5)
    channel_hopper.stop()


def test_channel_hopper_default_values():
    expected_channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    expected_sleep_time = 2
    actual = ChannelHopper([""])
    assert expected_channels == actual.channels
    assert expected_sleep_time == actual.sleep_time


def test_channel_hopper_uses_given_values():
    expected_channels = [1000, 1001]
    expected_sleep_time = 7
    actual = ChannelHopper([""], expected_channels, expected_sleep_time)
    assert expected_channels == actual.channels
    assert expected_sleep_time == actual.sleep_time


def test_channel_hopper_start_creates_hopper_process():
    channel_hopper = ChannelHopper([""])
    channel_hopper.start()
    time.sleep(1)
    assert channel_hopper.hopper_process is not None
    assert channel_hopper.hopper_process.is_alive()
    channel_hopper.stop()

def test_channel_hopper_stop_terminates_hopper_process():
    channel_hopper = ChannelHopper([""])
    channel_hopper.start()
    assert channel_hopper.hopper_process.exitcode is None
    channel_hopper.stop()
    time.sleep(1)
    assert channel_hopper.hopper_process.exitcode is not None
