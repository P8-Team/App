from enum import Enum
import pandas as pd
import numpy as np
import tsfresh.feature_extraction.settings

from src.wifi.wifi_frame import WifiFrame
from tsfresh import extract_relevant_features
from tsfresh import extract_features, select_features
from tsfresh.feature_extraction import ComprehensiveFCParameters
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from tsfresh.utilities.dataframe_functions import impute
from tsfresh.feature_selection.relevance import calculate_relevance_table
from src.multiprocess_wifi_listener import frames_from_file_with_caching

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

        # Return the most common classification of all the frames as a single label(based on labels gained in training)
        # Returns an error if the model has not been fitted
        return max(set(self.model.predict(features)), key=self.model.predict(features).count)

    def classify_interval_confidence(self, frames):
        # Extract relevant features using tsfresh and a custom setting created during training
        features = extract_features(frames, column_id='transmitter_address', column_sort='radio_timestamp',
                                    default_fc_parameters=self.feature_parameters)

        # Array of the probability for each label for each frame.
        prediction = self.model.predict_proba(features)

        # Summation of all frames.
        summation = prediction.sum(axis=0)

        # Returns the confidence for a given classification as a percentage.
        return max(summation)/np.sum(summation)

    def labels_in_model(self):
        # Returns an array with the labels of the trained model.
        return self.model.classes_

    def _verify_item_is_frame(self, item):
        """
        This method raises an error if the given item is not a frame
        """
        if not isinstance(item, WifiFrame):
            raise ValueError('classify must be given generator that produces elements of type Frame')

    def train(self, data, labels):
        # Extract relevant features using tsfresh
        #features = extract_relevant_features(data, labels, column_id='transmitter_address', column_sort='sniff_timestamp_0',
        #                                 default_fc_parameters=ComprehensiveFCParameters())

        #extracted_features = extract_features(data, column_id='transmitter_address', column_sort='sniff_timestamp_0',
        #             default_fc_parameters=ComprehensiveFCParameters(), impute_function=impute)

        #res = calculate_relevance_table(extracted_features, labels)

        #features = select_features(extracted_features, labels)
        # Creates a setting object, used to filter features during classify_interval.
        #self.feature_parameters = tsfresh.feature_extraction.settings.from_columns(features)

        # Split the data into training and test data
        input_train, input_test, labels_train, labels_test = train_test_split(data, labels)

        self.model.fit(input_train, labels_train)

        res = classification_report(labels_test, self.model.predict(input_test))
        print(res)

        return res

    def preprocess_data(self, df, labels):
        # Select rows that contain data from one of the devices with a label
        df = df[df['transmitter_address'].map(lambda x: labels.Address.str.contains(x).sum() == 1)]

        # This is how the labels should be computed when using tsfresh
        #correct_labels = labels.set_index('Address')

        # Create a serie containing a label for each row
        label_series = pd.DataFrame(df['transmitter_address']).set_index('transmitter_address').join(labels.set_index('Address')).squeeze()
        # Drop radio timestamp as it is NaN for the file data
        df = df.drop(['radio_timestamp'], axis='columns')
        #df['sniff_timestamp_0'] = pd.to_datetime(df['sniff_timestamp_0'],unit='s')
        # TODO: Change representation fo receiver_address to something like one hot encoding
        df = df.drop(['receiver_address', 'transmitter_address'], axis='columns')

        return df, label_series

    def load_files(self, files):
        dfs = list()
        for file in files:
            dfs.append(frames_from_file_with_caching(file))

        return pd.concat(dfs)
