import pytest
from src.behaviour import Frame, Classifier, Label

def generator(items: list):
  for item in items:
    yield item

def test_classifier_returns_one_result_for_each_interval():
  frames = generator([
    Frame(1), Frame(2), Frame(2), Frame(2), Frame(3), Frame(3), Frame(6)
  ])

  assert list(Classifier(1).classify(frames)) == [Label.Ok, Label.Undesired, Label.Ok]

def test_classify_returns_undesired_if_given_more_than_2_frames():
  frames = generator([Frame(1), Frame(1), Frame(1), Frame(3)])
  assert list(Classifier(1).classify(frames)) == [Label.Undesired]

def test_classify_returns_ok_if_given_2_frames():
  frames = generator([Frame(1), Frame(1), Frame(3)])
  assert list(Classifier(1).classify(frames)) == [Label.Ok]

def test_classify_returns_ok_if_given_less_than_2_frames():
  frames = generator([Frame(1), Frame(3)])
  assert list(Classifier(1).classify(frames)) == [Label.Ok]

def test_classify_throws_exception_if_given_generator_that_does_not_produce_frames():
  with pytest.raises(ValueError):
    list(Classifier(1).classify(generator([2, 'string'])))