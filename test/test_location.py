import pytest
from sympy import Circle, Point

from src.location import common_intersection, location, angle_between_two_points

def test_common_intersection_returns_point_where_three_circles_overlap():
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

def test_common_intersection_four_circles():
  circles = [
    Circle(Point(0,0), 5),
    Circle(Point(9,0), 4),
    Circle(Point(5,-5), 5),
    Circle(Point(5, 5), 5)
  ]

  assert common_intersection(circles) == Point(5,0)

def test_common_intersection_returns_None_when_three_circles_do_not_overlap():
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

def test_location_returns_point_based_on_three_reference_values():
  values = [
    [0,0,5],
    [9,0,4],
    [5,-5,5]
  ]

  assert location(values) == Point(5,0)

def test_location_returns_point_based_on_two_reference_values():
  values = [
    [0,0,5],
    [9,0,4],
  ]

  assert location(values) == Point(5,0)

def test_location_returns_point_based_on_four_reference_values():
  values = [
    [0,0,5],
    [9,0,4],
    [5,-5,5],
    [5,5,5]
  ]

  assert location(values) == Point(5,0)

def test_location_returns_None_when_no_location_can_be_determined():
  values = [
    [0,0,2],
    [9,0,4],
    [5,-5,2]
  ]

  assert location(values) == None

def test_angle_between_two_points_return_correct_angle_in_degrees():
  assert angle_between_two_points(Point(0,0), Point(15, 0)) == 0
  assert angle_between_two_points(Point(0,0), Point(5, 5)) == 45
  assert angle_between_two_points(Point(0,0), Point(0, 5.5)) == 90
  assert angle_between_two_points(Point(0,0), Point(-6.6, 0)) == 180
  assert angle_between_two_points(Point(0,0), Point(0, -82)) == 270
  