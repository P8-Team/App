from sympy import Point, Circle

from src.utils import is_point


def circle_factory(point: Point, radius: float):
    """

    :param point: Takes an input of the type sympy.Point
    :param radius: Takes a radius of the circle.
    :return: A circle.
    """
    if not is_point(point):
        raise TypeError("First argument must be a sympy.Point.")
    if not (isinstance(radius, float) or isinstance(radius, int)):
        raise TypeError("Second argument must be a number.")
    return Circle(point, radius)


def circle_factory_lst(circles: list):
    """
    Takes a list of elements, and converts them into circles.
    :param circles: Takes a list of arrays of the form [X,Y,Radius]
    :return: List of circles
    """
    for elem in circles:
        if len(elem) < 3:
            raise TypeError("Array does not contain all values")
        circle_factory(Point(elem[0], elem[1]), elem[2])
