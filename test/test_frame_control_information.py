from src.frame_control_information import FrameControlInformation
from test.utils.wifi_test_utils import Layer
import pandas as pd

def test_construct_frame_control_information():
    # Arrange
    layer = Layer({
        'wlan.fc.type': '1',
        'wlan.fc.subtype': '11',
        'wlan.ra_resolved': 'b4:de:31:9c:f0:8b',
        'wlan.ta_resolved': '50:e0:85:3f:77:5d'
    })

    # Act
    frame_control_information = FrameControlInformation.from_layer(layer)

    # Assert
    assert frame_control_information.type == 1
    assert frame_control_information.subtype == 11
    assert frame_control_information.receiver_address == 'b4:de:31:9c:f0:8b'
    assert frame_control_information.transmitter_address == '50:e0:85:3f:77:5d'


def test_construct_frame_control_information_missing_fields():
    # Arrange
    layer = Layer({
        'wlan.fc.type': '1',
        'wlan.ra_resolved': 'b4:de:31:9c:f0:8b'
    })

    # Act
    frame_control_information = FrameControlInformation.from_layer(layer)

    # Assert
    assert frame_control_information.type == 1
    assert frame_control_information.subtype is None
    assert frame_control_information.receiver_address == 'b4:de:31:9c:f0:8b'
    assert frame_control_information.transmitter_address is None


def test_compare_frame_control_information_identical():
    # Arrange
    layer1 = Layer({
        'wlan.fc.type': '1',
        'wlan.fc.subtype': '11',
        'wlan.ra_resolved': 'b4:de:31:9c:f0:8b',
        'wlan.ta_resolved': '50:e0:85:3f:77:5d'
    })
    layer2 = Layer({
        'wlan.fc.type': '1',
        'wlan.fc.subtype': '11',
        'wlan.ra_resolved': 'b4:de:31:9c:f0:8b',
        'wlan.ta_resolved': '50:e0:85:3f:77:5d'
    })

    # Act
    frame_control_information1 = FrameControlInformation.from_layer(layer1)
    frame_control_information2 = FrameControlInformation.from_layer(layer2)

    # Assert
    assert frame_control_information1 == frame_control_information2


def test_compare_frame_control_information_different():
    # Arrange
    layer1 = Layer({
        'wlan.fc.type': '1',
        'wlan.fc.subtype': '11',
        'wlan.ra_resolved': 'b4:de:31:9c:f0:8b',
        'wlan.ta_resolved': '50:e0:85:3f:77:5d'
    })
    layer2 = Layer({
        'wlan.fc.type': '0',
        'wlan.fc.subtype': '10',
        'wlan.ra_resolved': 'b4:de:31:9c:f0:8a',
        'wlan.ta_resolved': '50:e0:85:3f:77:5e'
    })

    # Act
    frame_control_information1 = FrameControlInformation.from_layer(layer1)
    frame_control_information2 = FrameControlInformation.from_layer(layer2)

    # Assert
    assert frame_control_information1 != frame_control_information2

def test_frame_control_information_to_dataframe():
    expected = pd.DataFrame(data = 
        {
         'type': [0],
         'subtype': [10],
         'receiver_address': ['b4:de:31:9c:f0:8a'],
         'transmitter_address': ['50:e0:85:3f:77:5e']
        })

    frame_control_information = FrameControlInformation(0, 10, 'b4:de:31:9c:f0:8a', '50:e0:85:3f:77:5e')

    actual = frame_control_information.to_dataframe()

    pd.testing.assert_frame_equal(actual, expected)
    