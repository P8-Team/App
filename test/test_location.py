from typing import Type
import pytest
from sympy import Circle, Point

from src.location import common_intersection

def test_comon_intersection_returns_point_where_three_circles_overlap():
  circles = [
    Circle(Point(0,0), 5),
    Circle(Point(9,0), 4),
    Circle(Point(5,-5), 5)
  ]

  assert common_intersection(circles) == Point(5,0)

def test_comon_intersection_two_circles():
  circles = [
    Circle(Point(0,0), 5),
    Circle(Point(9,0), 4)
  ]

  assert common_intersection(circles) == Point(5,0)

def test_comon_intersection_four_circles():
  circles = [
    Circle(Point(0,0), 5),
    Circle(Point(9,0), 4),
    Circle(Point(5,-5), 5),
    Circle(Point(5, 5), 5)
  ]

  assert common_intersection(circles) == Point(5,0)

def test_comon_intersection_returns_None_when_three_circles_do_not_overlap():
  circles = [
    Circle(Point(0,0), 2),
    Circle(Point(9,0), 4),
    Circle(Point(5,-5), 2)
  ]

  assert common_intersection(circles) == None

def test_common_intersection_throws_exception_if_not_given_list_of_circles():
  with pytest.raises(TypeError):
    common_intersection('this is not a list')
  with pytest.raises(TypeError):
    common_intersection([1, Point(3,3), 'not a circle'])

def test_common_intersection_throws_exception_if_given_less_than_two_circles():
  with pytest.raises(ValueError):
    common_intersection([Circle(Point(3,3),3)])