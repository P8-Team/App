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


def test_channel_hopper_uses_given_channels():
    expected = [1000, 1001]
    channel_hopper = ChannelHopper([""], expected)
    actual = channel_hopper.channels
    assert expected == actual
