import pytest
from sympy import Point

from src.Circle_factory import circle_factory
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
