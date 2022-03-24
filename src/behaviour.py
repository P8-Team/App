from enum import Enum
from src.utils import is_list_of_type

# Enum defining the possible results of classify
Label = Enum('Label', 'Ok Undesired')

class Frame:
    def __init__(self, timestamp):
        self.id = 0
        self.signal_strength = []
        self.frame_length = 0
        self.transmitter_mac_address = 0
        self.timestamp = timestamp

class Classifier:
    """
    A class for classifying the behavior of IoT devices
    """
    def __init__(self, interval_seconds):
        """
        :param interval_seconds: The amount of time in seconds to aggregate frames to classify 
        """
        self.interval = interval_seconds

    def classify(self, frame_gen):
        """
        Classifies the behaviour of an IoT device based on a number of frames within a time interval
        Note: This is a generator that yields an item for each time interval.
            An item first yielded when a frame that is in the next interval is received from frame_gen

        :param frame_gen: A generator that produces frames
        """ 
        first = next(frame_gen)
        if not isinstance(first, Frame):
            raise ValueError('classify must be given generator that produces elements of type Frame')
        interval_end = first.timestamp + self.interval
        frames_in_interval = [first]
        for frame in frame_gen:
            if not isinstance(frame, Frame):
                raise ValueError('classify must be given generator that produces elements of type Frame')
                
            if frame.timestamp > interval_end:
                result = self.classify_interval(frames_in_interval)
                frames_in_interval = list()
                interval_end = frame.timestamp + self.interval
                yield result
            else:
                frames_in_interval.append(frame)  

    def classify_interval(self, frames):
        if not is_list_of_type(frames, Frame):
            raise ValueError('classify_interval must be given list with elements of type Frame')

        # Classify behaviour
        return Label.Ok if len(frames) <= 2 else Label.Undesired
