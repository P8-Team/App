from sympy import Circle, Point2D, Point

from src.location import common_intersection

def test_comon_intersection_returns_point_where_three_circles_overlap():
  circles = [
    Circle(Point(0,0), 5),
    Circle(Point(9,0), 4),
    Circle(Point(5,-5), 5)
  ]

  assert common_intersection(circles) == Point2D(5,0)

def test_comon_intersection_returns_None_when_three_circles_do_not_overlap():
  circles = [
    Circle(Point(0,0), 2),
    Circle(Point(9,0), 4),
    Circle(Point(5,-5), 2)
  ]

  assert common_intersection(circles) == None