from distutils.util import change_root
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

def test_channel_hopper_sets_interfaces():
    channel_hopper = ChannelHopper(['1','2','3'])

    assert channel_hopper.interfaces == ['1','2','3']

def test_channel_hopper_default_channels():
    channel_hopper = ChannelHopper([''])

    assert channel_hopper.channels == [1,2,3,4,5,6,7,8,9,10,11,12,13]

def test_channel_hopper_uses_given_channels():
    expected = [1000, 1001]
    channel_hopper = ChannelHopper([""], expected)
    actual = channel_hopper.channels
    assert expected == actual

def test_channel_hopper_default_sleep_time():
    channel_hopper = ChannelHopper([''])

    assert channel_hopper.sleep_time == 2

def test_channel_hopper_uses_given_time_between_hops():
    channel_hopper = ChannelHopper([''], time_between_hops_sec= 87.2)

    assert channel_hopper.sleep_time == 87.2