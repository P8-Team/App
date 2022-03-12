import pytest
from src.utils import *

class TestClass():
  pass

def test_is_list():
  assert is_list(1) == False
  assert is_list('hello') == False
  assert is_list({'test': 'dict'}) == False
  assert is_list(('elem1', 2)) == False

  assert is_list([]) == True
  assert is_list(['one', 2, (3, 'four')])

def test_is_type():
  assert is_type(3) == False
  assert is_type([1,2,3]) == False

  assert is_type(TestClass) == True
  assert is_type(int) == True
  assert is_type(dict) == True
  
def test_is_list_of_type_empty_list_always_returns_true():
  """Given an empty list is_list_of_type should return true for any type"""
  assert is_list_of_type([], int) == True 
  assert is_list_of_type([], dict) == True 
  assert is_list_of_type([], list) == True 
  assert is_list_of_type([], tuple) == True 
  assert is_list_of_type([], float) == True
  assert is_list_of_type([], TestClass) == True 
  
def test_is_list_of_type_throws_exception_if_not_given_list():
  with pytest.raises(TypeError):
    is_list_of_type(1, int)
  with pytest.raises(TypeError):
    is_list_of_type({1: 'one'}, TestClass)
  with pytest.raises(TypeError):
    is_list_of_type('this is not a list', list)

def test_is_list_of_type_throws_exception_if_not_given_type():
  with pytest.raises(TypeError):
    is_list_of_type([], 2)
  with pytest.raises(TypeError):
    is_list_of_type([1,2,3], 'not a type')

def test_is_list_of_type():
  assert is_list_of_type([1,2,3,4], int) == True
  assert is_list_of_type([TestClass(), TestClass()], TestClass) == True
  assert is_list_of_type([[1], [], [3]], list) == True

  assert is_list_of_type([1,2,3,4], TestClass) == False
  assert is_list_of_type([1,2,'three',4], int) == False
  assert is_list_of_type([{1:2}, [], {3:4}], dict) == False
  
