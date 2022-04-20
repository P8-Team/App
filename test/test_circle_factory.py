import pytest
from sympy import Point, Circle
from fractions import Fraction
from src.location.circle_factory import circle_factory, circle_factory_lst
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

def test_circle_factory_returns_circle_with_correct_values():
    circle1 = circle_factory(Point(1,2),3)
    circle2 = circle_factory(Point(47.2, 800.99), 567.567)
    assert circle1.center == Point(1,2)
    assert circle2.center == Point(47.2, 800.99)
    assert circle1.radius == 3
    assert circle2.radius == Fraction(567567,1000)

def test_circle_factory_lst_throws_exception_if_elements_are_incorrect():
    with pytest.raises(ValueError):
        circle_factory_lst([[1,2]])
    with pytest.raises(ValueError):
        circle_factory_lst([[1,2,3,4]])
    with pytest.raises(ValueError):
        circle_factory_lst([[1,2,3], [4,5,6], [7,8]])
    with pytest.raises(ValueError):
        circle_factory_lst([[1,'string',3]])

def test_circle_factory_lst_returns_list_of_circles():
    assert circle_factory_lst([[1,2,3], [4,5,6]]) == [Circle(Point(1,2), 3), Circle(Point(4,5), 6)]
    assert circle_factory_lst([[1.1, 11.35, 899], [4,5,6]]) == [Circle(Point(1.1,11.35), 899), Circle(Point(4,5), 6)]
