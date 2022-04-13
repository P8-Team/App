import pytest
from src.classifier import Classifier, Label

# Function for turning list into generator
from test.utils.wifi_frame_factory import frame_factory


def generator(items: list):
  for item in items:
    yield item

def test_classifier_returns_one_result_for_each_interval():
  frames = generator([
    frame_factory(1),
    frame_factory(2),
    frame_factory(2),
    frame_factory(2),
    frame_factory(3),
    frame_factory(3),
    frame_factory(6),
  ])

  assert list(Classifier(1).classify(frames)) == [Label.Ok, Label.Undesired, Label.Ok]

def test_classify_returns_undesired_if_given_more_than_2_frames():
  frames = generator([frame_factory(1), frame_factory(1), frame_factory(1), frame_factory(3)])
  assert list(Classifier(1).classify(frames)) == [Label.Undesired]

def test_classify_returns_ok_if_given_2_frames():
  frames = generator([frame_factory(1), frame_factory(1), frame_factory(3)])
  assert list(Classifier(1).classify(frames)) == [Label.Ok]

def test_classify_returns_ok_if_given_less_than_2_frames():
  frames = generator([frame_factory(1), frame_factory(3)])
  assert list(Classifier(1).classify(frames)) == [Label.Ok]

def test_classify_throws_exception_if_given_generator_that_does_not_produce_frames():
  with pytest.raises(ValueError):
    list(Classifier(1).classify(generator([2, 'string'])))