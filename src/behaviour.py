from enum import Enum
from src.utils import is_list_of_type

# Enum defining the possible results of classify
Label = Enum('Label', 'Ok Undesired')

class Frame:
  def __init__(self):
        self.id = 0
        self.signal_strength = []
        self.frame_length = 0
        self.transmitter_mac_address = 0

class Classifier:
  def classify(self, frames: list):
    # Check that arguments are arguments
    if len(frames) == 0:
      raise ValueError('classify must given non-empty list of frames')
    if not is_list_of_type(frames, Frame):
      raise ValueError('classify must be given list with elements of type Frame')

    # Classify behaviour
    return Label.Ok if len(frames) <= 2 else Label.Undesired