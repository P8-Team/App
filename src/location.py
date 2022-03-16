from sympy import Circle, Point

def common_intersection(circles):
  intersection1 = circles[0].intersection(circles[1])
  intersection2 = circles[1].intersection(circles[2])

  result = list(set(intersection1).intersection(intersection2))
  if len(result) == 0:
    return None
  else:
    return result[0]