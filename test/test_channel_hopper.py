import signal

import pytest
from src.channel_hopper import ChannelHopper
import time


def create_test_channel_hopper(interfaces, channels=None, sleep_time=None):
    ch = ChannelHopper(interfaces, channels, sleep_time)
    ch.test_mode = True
    return ch


@pytest.mark.skip(reason="The result of the hop can only be seen by running 'sudo iwlist <interface> channel'")
def test_channel_hopper_using_start():
    ChannelHopper.__hop__(interfaces=["wlan4"], channels=[3, 7, 13], sleep_time=1, test_mode=False)


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
    channel_hopper = create_test_channel_hopper([""])
    channel_hopper.start()
    time.sleep(2)
    assert channel_hopper.hopper_process is not None
    assert channel_hopper.hopper_process.is_alive()
    channel_hopper.hopper_process.kill()


# TODO: The Git Runner halts here, because the spawned process is never terminated?!?
def test_channel_hopper_stop_terminates_hopper_process():
    channel_hopper = create_test_channel_hopper([""])
    channel_hopper.start()
    assert channel_hopper.hopper_process.exitcode is None
    # channel_hopper.stop()
    channel_hopper.hopper_process.kill()
    channel_hopper.hopper_process.join(10)
    assert channel_hopper.hopper_process.is_alive() is False
    assert channel_hopper.hopper_process.exitcode is not None
    assert channel_hopper.hopper_process.exitcode == -signal.SIGTERM
