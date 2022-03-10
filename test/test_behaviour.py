from src.behaviour import Frame, Classifier, Label

def test_classify_returns_undesired_if_given_more_than_2_frames():
  frames = [Frame(), Frame(), Frame()]
  assert Classifier().classify(frames) == Label.Undesired

def test_classify_returns_ok_if_given_2_frames():
  frames = [Frame(), Frame()]
  assert Classifier().classify(frames) == Label.Ok

def test_classify_returns_ok_if_given_less_than_2_frames():
  frames = [Frame()]
  assert Classifier().classify(frames) == Label.Ok