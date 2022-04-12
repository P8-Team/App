import pytest
from src.channel_hopper import ChannelHopper
import time

@pytest.mark.skip(reason="The result of the test can only be seen by running some commands")
def test_channel_hopper_using_start():
    channel_hopper = ChannelHopper(["wlan4"])
    channel_hopper.start()
    time.sleep(5)
    channel_hopper.stop()