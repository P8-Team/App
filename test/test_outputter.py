import json

from sympy import Point

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
    elements = [Point(1, 2), Point(1, 3)]
    result = output_formatter(elements, __serializer_for_test_point)
    assert result == "1213"


def test_output_function_returns_correct_information():
    elements = ['a', 'b', 'c']
    output_test = list()
    outputter(elemnts, json.dumps, __output_test_function, output_test)
    # output_test[0] is needed, as the output_test is a tuple which, and only the first element is relevant.
    assert output_test[0] == '["a", "b", "c"]'
