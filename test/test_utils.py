import types

import pytest
from sympy import Circle, Point

from src.utils import is_list, is_list_of_type, is_type, is_circle, is_point, true_for_all, verify_type, \
    chain_generators


class TestClass():
    pass


def test_is_list():
    assert is_list(1) == False
    assert is_list('hello') == False
    assert is_list({'test': 'dict'}) == False
    assert is_list(('elem1', 2)) == False

    assert is_list([]) == True
    assert is_list(['one', 2, (3, 'four')])


def test_is_type():
    assert is_type(3) == False
    assert is_type([1, 2, 3]) == False

    assert is_type(TestClass) == True
    assert is_type(int) == True
    assert is_type(dict) == True


def test_is_list_of_type_empty_list_always_returns_true():
    """Given an empty list is_list_of_type should return true for any type"""
    assert is_list_of_type([], int) == True
    assert is_list_of_type([], dict) == True
    assert is_list_of_type([], list) == True
    assert is_list_of_type([], tuple) == True
    assert is_list_of_type([], float) == True
    assert is_list_of_type([], TestClass) == True


def test_is_list_of_type_throws_exception_if_not_given_list():
    with pytest.raises(TypeError):
        is_list_of_type(1, int)
    with pytest.raises(TypeError):
        is_list_of_type({1: 'one'}, TestClass)
    with pytest.raises(TypeError):
        is_list_of_type('this is not a list', list)


def test_is_list_of_type_throws_exception_if_not_given_type():
    with pytest.raises(TypeError):
        is_list_of_type([], 2)
    with pytest.raises(TypeError):
        is_list_of_type([1, 2, 3], 'not a type')


def test_is_list_of_type():
    assert is_list_of_type([1, 2, 3, 4], int) == True
    assert is_list_of_type([TestClass(), TestClass()], TestClass) == True
    assert is_list_of_type([[1], [], [3]], list) == True

    assert is_list_of_type([1, 2, 3, 4], TestClass) == False
    assert is_list_of_type([1, 2, 'three', 4], int) == False
    assert is_list_of_type([{1: 2}, [], {3: 4}], dict) == False


def test_is_point():
    assert is_point(Point(1, 2, 3)) == True
    assert is_point(Point(2, 3)) == True

    assert is_point(3) == False
    assert is_point([1, 2]) == False
    assert is_point('no a point') == False


def test_is_circle():
    assert is_circle(Circle(Point(2, 2), 2)) == True
    assert is_circle(Circle(Point(0, 0), Point(1, 1), Point(1, 0))) == True

    assert is_circle(Point(2, 2)) == False
    assert is_circle(2) == False
    assert is_circle([1, 2]) == False
    assert is_circle('no a circle') == False


def test_true_for_all_returns_true_given_empty_list():
    assert true_for_all(lambda x: False, []) == True
    assert true_for_all(lambda x: True, []) == True


def test_true_for_all_returns_true_if_condition_hold_for_all():
    assert true_for_all(lambda x: x < 10, [1, 2, 3, 4]) == True
    assert true_for_all(lambda x: x % 3 == 0, [3, 6, 9, 81]) == True


def test_true_for_all_return_false_if_condition_fails():
    assert true_for_all(lambda x: x == 1, [1, 2, 1, 1, 1]) == False
    assert true_for_all(lambda x: x < 0, [1, 2, 3, 4]) == False


def test_true_for_all_throws_exception_if_second_argument_is_not_list():
    with pytest.raises(TypeError):
        true_for_all(lambda x: True, 'not a list')


def test_true_for_all_throws_exception_if_first_argument_is_not_function():
    with pytest.raises(TypeError):
        true_for_all('Not a function', [])


# Helper function for turning list into generator
def generator(items: list):
    for item in items:
        yield item


def test_verify_type_returns_none_if_given_item_with_correct_type():
    assert verify_type(int, 1) == None
    assert verify_type(list, [1, 2, 3]) == None
    assert verify_type(types.GeneratorType, generator([1, 2, 3])) == None


def test_verify_type_throws_exception_if_given_item_with_incorrect_type():
    with pytest.raises(TypeError):
        verify_type(int, 'string')
    with pytest.raises(TypeError):
        verify_type(types.GeneratorType, generator)
    with pytest.raises(TypeError):
        verify_type(list, generator([1, 2, 3, 4]))


def test_verify_type_accepts_optional_parameter_that_becomes_message_prefix():
    with pytest.raises(TypeError) as ex:
        verify_type(int, 'string', 'test prefix')
        assert ex.value.startswith('test prefix') == True


def test_verify_type_throws_exception_if_optional_parameter_is_not_string():
    with pytest.raises(TypeError):
        verify_type(int, 1, ['not a string'])


def test_chain_generators_chains_generators():
    gen1 = (i for i in range(0, 2))
    gen2 = (i for i in range(2, 5))

    assert list(chain_generators(gen1, gen2)) == [0, 1, 2, 3, 4]
