from sympy import Circle
from src.utils import is_list_of_type
from src.Circle_factory import circle_factory_lst
import itertools

def location(reference_values):
  """
  Determine a position based on the distance from a number of reference_values
  :param reference_values: List of lists containing position and distance. (Each elements has the form [x, y, dist])
  :return: Point representing the location
  """
  return common_intersection(circle_factory_lst(reference_values))

def common_intersection(circles):
  if not is_list_of_type(circles, Circle):
    raise TypeError('common_intersection must be given a list of Circles')
  if len(circles) < 2:
    raise ValueError('common_intersection must be given at least two Circles')

  # Find intersections of the first two circles
  intersections = set(compare(circles[0], circles[1]))

  # Find intersections of all pairs of circles
  # Take set intersection of the previous values and the new values
  # This will ensure that the result set will only contain points where all the circles intersect
  for a, b in itertools.combinations(circles, 2):
    intersections.intersection(compare(a, b))

  result = list(intersections)

  if len(result) > 0:
    return result[0]
  else:
    return None

def compare(a, b):
  return set(a.intersection(b))