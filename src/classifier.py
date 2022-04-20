from enum import Enum
import pandas as pd
import numpy as np
import tsfresh.feature_extraction.settings

from src.wifi.wifi_frame import WifiFrame
from tsfresh import extract_relevant_features
from tsfresh import extract_features
from tsfresh.feature_extraction import ComprehensiveFCParameters
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

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
        self.model = RandomForestClassifier()
        self.feature_parameters = None  # tsfresh settings object, used in train and classify_interval

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
        # Extract relevant features using tsfresh and a custom setting created during training
        features = extract_features(frames, column_id='transmitter_address', column_sort='radio_timestamp',
                                            default_fc_parameters=self.feature_parameters)

        # Returns the identity(based on labels from training)
        # Returns an error if the model has not been fitted
        return np.argmax(self.model.predict(features))

        # OLD CODE - Kept for testing, see test_behaviour
        # return Label.Ok if len(frames) <= 2 else Label.Undesired

    def classify_interval_confidence(self, frames):
        # Extract relevant features using tsfresh and a custom setting created during training
        features = extract_features(frames, column_id='transmitter_address', column_sort='radio_timestamp',
                                    default_fc_parameters=self.feature_parameters)

        # Array of the probability for each label for each frame.
        prediction = self.model.predict_proba(features)

        prediction_confidence = prediction.sum(axis=0)
        prediction_labels = self.model.classes_

        # Return the confidence for a given classification.


    def _verify_item_is_frame(self, item):
        """
        This method raises an error if the given item is not a frame
        """
        if not isinstance(item, WifiFrame):
            raise ValueError('classify must be given generator that produces elements of type Frame')

    def train(self, data, labels):
        # Extract relevant features using tsfresh
        features = extract_relevant_features(data, labels, column_id='transmitter_address', column_sort='radio_timestamp',
                                         default_fc_parameters=ComprehensiveFCParameters())

        # Creates a setting object, used to filter features during classify_interval.
        self.feature_parameters = tsfresh.feature_extraction.settings.from_columns(features)

        # Split the data into training and test data
        input_train, input_test, labels_train, labels_test = train_test_split(features, labels)

        self.model.fit(input_train, labels_train)

        res = classification_report(labels_test, self.model.predict(input_test))
        print(res)

        return res

        