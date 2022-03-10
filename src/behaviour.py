from enum import Enum

Label = Enum('Label', 'Ok Undesired')

class Frame:
  def __init__(self):
        self.id = 0
        self.rssi = []
        self.packet_length = 0
        self.mac_address = 0


class Classifier:
  def classify(self, frames: list):
    # Check that arguments are arguments
    if len(frames) == 0:
      raise ValueError('classify must given non-empty list of frames')
    if any(not isinstance(item, Frame) for item in frames):
      raise ValueError('classify must be given list with elements of type Frame')

    # Classify behaviour
    return Label.Ok if len(frames) <= 2 else Label.Undesired