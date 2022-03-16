from src.frame_control_information import FrameControlInformation
from test.utils.wifi_test_utils import Layer


def test_construct_frame_control_information():
    # Arrange
    layer = Layer({
        'wlan.fc.type': '1',
        'wlan.fc.subtype': '11',
        'wlan.ra_resolved': 'b4:de:31:9c:f0:8b',
        'wlan.ta_resolved': '50:e0:85:3f:77:5d'
    })

    # Act
    frame_control_information = FrameControlInformation(layer)

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
    frame_control_information = FrameControlInformation(layer)

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
    frame_control_information1 = FrameControlInformation(layer1)
    frame_control_information2 = FrameControlInformation(layer2)

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
    frame_control_information1 = FrameControlInformation(layer1)
    frame_control_information2 = FrameControlInformation(layer2)

    # Assert
    assert frame_control_information1 != frame_control_information2
