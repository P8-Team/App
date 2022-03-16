from sympy import Circle, Point
from src.utils import is_list_of_type

def common_intersection(circles):
  if not is_list_of_type(circles, Circle):
    raise TypeError('common_intersection must be given a list of Circles')
    
  intersection1 = circles[0].intersection(circles[1])
  intersection2 = circles[1].intersection(circles[2])

  result = list(set(intersection1).intersection(intersection2))
  if len(result) == 0:
    return None
  else:
    return result[0]