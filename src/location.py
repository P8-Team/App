from sympy import Circle
from src.utils import is_list_of_type
import itertools

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