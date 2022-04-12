import pytest
from src.channel_hopper import ChannelHopper


def test_basic_test_test():
    channel_hopper = ChannelHopper(["wlan4"])
    channel_hopper.hop()


