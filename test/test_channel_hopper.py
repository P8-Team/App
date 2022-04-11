import pytest
from src.channel_hopper import ChannelHopper


def test_basic_test_test():
    channel_hopper = ChannelHopper(["interface1", "interface2", "interface3"])
    channel_hopper.hop()


