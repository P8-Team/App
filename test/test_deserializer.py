import pytest

from src import deserializer as ds
from src.Packet import Packet


def test_objectifier_correct_input():
    test_input = "01:02:03:04:ab:cd,b,c,d,e,f;01:02:03:04:ab:cf,e,l,o;"
    parsed_output = ds.parser(test_input)
    assert parsed_output[0].mac_address == "01:02:03:04:ab:cd"


def test_objectifier_correct_input_validate_id():
    base_line = Packet.identifier
    test_input = "01:02:03:04:ab:cd,b,c,d,e,f;01:02:03:04:ab:cf,e,l,o;"
    parsed_output = ds.parser(test_input)
    assert parsed_output[0].identifier == base_line + 1
    assert parsed_output[1].identifier == base_line + 2


def test_objectifier_incorrect_input_incorrect_mac_address():
    test_input = "definitely:not:a:mac:cd,b,c,d,e,f;g,e,l,o;"
    with pytest.raises(TypeError):
        ds.parser(test_input)


def test_objectifier_incorrect_input_not_all_fields_present():
    test_input = "a,b;g,e,l,o;"
    with pytest.raises(TypeError):
        ds.parser(test_input)
