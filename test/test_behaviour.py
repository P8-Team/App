from src.behaviour import Classifier, Label

def test_classify():
  assert Classifier().classify([]) == Label.Ok
