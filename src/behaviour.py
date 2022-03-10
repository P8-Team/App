from enum import Enum

Label = Enum('Label', 'Ok Undesired')

class Classifier:
  def classify(self, packets: list):
    return Label.Ok