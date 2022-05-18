import pytest

from src.device.device import Device
from src.oracle import Oracle


def test_oracle_device_given_identification():
    device_address_dict = {
        "00:00:01": [-23, "1"],
        "00:00:02": [18, "2"]
    }
    oracle = Oracle(device_address_dict)

    device_list = [
        Device("00:00:01", []),
        Device("00:00:02", []),
        Device("00:00:03", [])
    ]

    result = list(oracle.classify(device_list))

    assert result[0].identification[0] == -23
    assert result[0].identification[1] == "1"
    assert result[1].identification[0] == 18
    assert result[1].identification[1] == "2"
    assert result[2].identification is None