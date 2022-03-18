import pytest
from sympy import Point

from src.Circle_factory import circle_factory, circle_factory_lst
from src.utils import is_circle


def test_circle_factory_fails_incorrect_first_input():
    with pytest.raises(TypeError):
        circle_factory("a", 0)


def test_circle_factory_fails_incorrect_second_input():
    with pytest.raises(TypeError):
        circle_factory(Point(2, 2), "Wrong")


def test_circle_factory_returns_circle_gets_float_second_parameter():
    assert is_circle(circle_factory(Point(2, 2), 5.0))


def test_circle_factory_returns_circle_gets_int_second_parameter():
    assert is_circle(circle_factory(Point(2, 2), 5))


def test_circle_factory_lst_throws_exception_if_elements_are_incorrect():
    with pytest.raises(ValueError):
        circle_factory_lst([[1,2]])
    with pytest.raises(ValueError):
        circle_factory_lst([[1,2,3,4]])
    with pytest.raises(ValueError):
        circle_factory_lst([[1,2,3], [4,5,6], [7,8]])
