from sympy import Point, Circle

from src.utils import is_point, true_for_all


def circle_factory(point: Point, radius: float):
    """
    Creates a circle from a Point and a radius.
    Note: When using floats, the resulting values in Point and Circle
    objects will be converted to the type Fraction
    :param point: Takes an input of the type sympy.Point
    :param radius: Takes a radius of the circle.
    :return: A circle.
    """
    if not is_point(point):
        raise TypeError("First argument must be a sympy.Point.")
    # TODO: Create type checking function is_number in the utils module
    if not (isinstance(radius, float) or isinstance(radius, int)):
        raise TypeError("Second argument must be a number.")
    return Circle(point, radius)


def circle_factory_lst(circles: list):
    """
    Takes a list of elements, and converts them into circles.
    :param circles: Takes a list of lists of the form [X,Y,Radius]
    :return: List of circles
    """
    return list(map(circle_from_list, circles))
        
def circle_from_list(list: list):
    if len(list) != 3:
        raise ValueError("Elements must be lists containing three elements")
    if not true_for_all(lambda elem: isinstance(elem, float) or isinstance(elem, int), list):
        raise ValueError("All elements of list must be numbers")
    return circle_factory(Point(list[0], list[1]), list[2])
