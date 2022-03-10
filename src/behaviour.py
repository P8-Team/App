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
    return Label.Ok if len(frames) <= 2 else Label.Undesired