from turtle import circle
from sympy import Circle
from src.utils import is_list_of_type
import itertools

def common_intersection(circles):
  if not is_list_of_type(circles, Circle):
    raise TypeError('common_intersection must be given a list of Circles')
  if len(circles) < 2:
    raise ValueError('common_intersection must be given at least two Circles')

  intersections = set(compare(circles[0], circles[1]))

  for a, b in itertools.combinations(circles[2:], 2):
    intersections.update(set(compare(a, b)))

  result = list(intersections)

  if len(result) > 0:
    return result[0]
  else:
    return None

def compare(a, b):
  return a.intersection(b)