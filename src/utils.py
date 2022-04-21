from types import FunctionType
from sympy import Circle, Point

def is_list(object) -> bool:
  return isinstance(object, list)

def is_type(object) -> bool:
  return isinstance(object, type)

def is_list_of_type(list: list, given_type: type) -> bool:
  if not is_list(list):
    raise TypeError('is_list_of_types must be given a list as first argument')
  if not is_type(given_type):
    raise TypeError('is_list_of_types must be given a type as second argument')
  return true_for_all(lambda item: isinstance(item, given_type), list)

def is_point(object):
  return isinstance(object, Point)

def is_circle(object):
  return isinstance(object, Circle)

def true_for_all(cond: FunctionType, list: list):
  if not isinstance(cond, FunctionType):
    raise TypeError('First argument must be a function')
  if not is_list(list):
    raise TypeError('Second argument must be a list')
  return all(cond(x) for x in list)

def verify_type(type, obj, prefix = ''):
  if not isinstance(prefix, str):
    raise TypeError('verify_type Expected type str but got ' + type(prefix))
  if not isinstance(obj, type):
    raise TypeError(prefix + ' Expected type ' + type + ' but got ' + type(obj))

def chain_generators(*iterables):
    for it in iterables:
        for element in it:
            yield element