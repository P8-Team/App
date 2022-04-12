from distutils.util import change_root
import pytest
from src.channel_hopper import ChannelHopper
import time


@pytest.mark.skip(reason="The result of the channel hopper can only be seen by "
                         "running 'sudo iwlist <interface> channel' and by looking at the console")
def test_channel_hopper_using_start():
    ChannelHopper.__hop__(interfaces=["wlan4"], channels=[3, 7, 13], sleep_time=1)


def test_channel_hopper_sets_interfaces():
    channel_hopper = ChannelHopper(['1', '2', '3'])

    assert channel_hopper.interfaces == ['1', '2', '3']


def test_channel_hopper_default_channels():
    channel_hopper = ChannelHopper([''])

    assert channel_hopper.channels == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


def test_channel_hopper_uses_given_channels():
    channel_hopper = ChannelHopper([''], channels=[2, 4, 6, 8888])

    assert channel_hopper.channels == [2, 4, 6, 8888]


def test_channel_hopper_default_sleep_time():
    channel_hopper = ChannelHopper([''])

    assert channel_hopper.sleep_time == 2


def test_channel_hopper_uses_given_time_between_hops():
    channel_hopper = ChannelHopper([''], time_between_hops_sec=87.2)

    assert channel_hopper.sleep_time == 87.2


def test_channel_hopper_start_creates_hopper_process():
    channel_hopper = ChannelHopper([""])
    channel_hopper.start()
    time.sleep(1)
    assert channel_hopper.hopper_process is not None
    assert channel_hopper.hopper_process.is_alive()
    channel_hopper.hopper_process.terminate()


def test_channel_hopper_stop_terminates_hopper_process():
    channel_hopper = ChannelHopper([""])
    channel_hopper.start()
    assert channel_hopper.hopper_process.exitcode is None
    channel_hopper.stop()
    time.sleep(1)
    assert channel_hopper.hopper_process.exitcode is not None
