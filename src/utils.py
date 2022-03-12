
def is_list(object) -> bool:
  return isinstance(object, list)

def is_type(object) -> bool:
  return isinstance(object, type)

def is_list_of_type(list: list, given_type: type) -> bool:
  if not is_list(list):
    raise TypeError('is_list_of_types must be given a list as first argument')
  if not is_type(given_type):
    raise TypeError('is_list_of_types must be given a type as second argument')
  return all(isinstance(item, given_type) for item in list)