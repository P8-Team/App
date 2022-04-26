from enum import Enum

from src.wifi.wifi_frame import WifiFrame

# Enum defining the possible results of classify
Label = Enum('Label', 'Ok Undesired')


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
        # Create generator that accumulates frames in an interval and yields lists of frames
        frame_acc = self.accumulate_frames(frame_gen)
        for frame_list in frame_acc:
            yield self.classify_interval(frame_list)

    def accumulate_frames(self, frame_gen):
        # Get first element of generator and use it to determine end of interval
        first = next(frame_gen)
        self._verify_item_is_frame(first)
        interval_end = first.wlan_radio.get_earliest_sniff_timestamp() + self.interval
        frames_in_interval = [first]
        for frame in frame_gen:
            self._verify_item_is_frame(frame)

            if frame.wlan_radio.get_earliest_sniff_timestamp() >= interval_end:
                yield frames_in_interval
                # Add frame to next interval use it to determine end of next interval
                frames_in_interval = [frame]
                interval_end = frame.wlan_radio.get_earliest_sniff_timestamp() + self.interval
            else:
                frames_in_interval.append(frame)

    def classify_interval(self, frames):
        # Classify behaviour
        return Label.Ok if len(frames) <= 2 else Label.Undesired

    def _verify_item_is_frame(self, item):
        """
        This method raises an error if the given item is not a frame
        """
        if not isinstance(item, WifiFrame):
            raise ValueError('classify must be given generator that produces elements of type Frame')
