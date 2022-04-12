import json

import pytest
from sympy import Point2D

from src.outputter import output_formatter, outputter


def __serializer_for_test_point(objects):
    output = ""
    for elem in objects:
        output += str(elem.x) + str(elem.y)
    return output


def __output_test_function(input_value, output_value):
    output_value[0].append(input_value)


def test_outputter_gives_correct_output_given_list_of_strings():
    elements = ["a", "b,c", "c"]
    result = output_formatter(elements, json.dumps)
    assert result == '["a", "b,c", "c"]'


def test_outputter_gives_correct_output_given_custom_serializer():
    elements = [Point2D(1, 2), Point2D(1, 3)]
    result = output_formatter(elements, __serializer_for_test_point)
    assert result == "1213"


def test_output_function_returns_correct_information():
    elements = ['a', 'b', 'c']
    output_test = list()
    outputter(elements, json.dumps, __output_test_function, output_test)
    # output_test[0] is needed, as the output_test is a tuple which, and only the first element is relevant.
    assert output_test[0] == '["a", "b", "c"]'


def test_outputter_function_one_variable():
    i = 0

    def __output_test_function_with_one_input(input_value):
        nonlocal i
        i = 10

    elements = ['a', 'b']
    outputter(elements, json.dumps, __output_test_function_with_one_input)

    assert i == 10


def test_output_formatter_raises_type_error_on_non_function_input():
    with pytest.raises(TypeError):
        output_formatter(['a,b,c'], "NotAFunction")


def test_outputter_raises_type_error_on_non_function_input():
    with pytest.raises(TypeError):
        outputter(['a,b,c'], print, "NotAFunction")
