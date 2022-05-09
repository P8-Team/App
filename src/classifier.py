import os
from typing import Iterable

import numpy as np
import pandas as pd
from joblib import dump, load
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from src.device.device import Device
from src.device_lookup import DeviceLookup
from src.multiprocess_wifi_listener import frames_from_file_with_caching, cache_dataframe
from src.wifi.wifi_frame import WifiFrame


class Classifier:
    """
    A class for classifying the behavior of IoT devices
    """

    def __init__(self, interval_seconds):
        """
        param interval_seconds: The amount of time in seconds to aggregate frames to classify
        """
        self.interval = interval_seconds
        self.model = RandomForestClassifier()

    def classify(self, generator: Iterable[Device]):
        """
        Identifies an IoT device based on a number of frames within a time interval
        Note: This is a generator that yields a label a single device, as a result of labeling time intervals.

        param device: A devices
        """
        device_lookup = DeviceLookup()

        for device in generator:
            interval_classification_with_threshold = list()

            # Accumulate frames from a device in intervals and produce a list with lists of label and confidence for
            # classification of an interval
            frame_acc = self.accumulate_frames(device.frames)
            for frame_list in frame_acc:
                interval_classification_with_threshold.append([self.classify_interval_label(frame_list),
                                                               self.classify_interval_confidence(frame_list)])
            if not interval_classification_with_threshold:
                yield device
                continue
            # Determines the classification of the device based on classification of frame intervals with high
            # confidence (>= 0.6)
            label = self.determine_device_classification(interval_classification_with_threshold)
            if label is None:
                yield device
                continue

            # Looks up transmission power and name of device
            device.identification = device_lookup.get_device_info_by_label(label)

            yield device

    def accumulate_frames(self, frames):
        """
        Accumulates frames for a single device into intervals of frames
        """
        # Get first element of frames and use it to determine end of interval
        frames = iter(frames)
        first = next(frames)
        self._verify_item_is_frame(first)
        interval_end = first.wlan_radio.get_earliest_sniff_timestamp() + self.interval
        frames_in_interval = [first]
        for frame in frames:
            self._verify_item_is_frame(frame)

            if frame.wlan_radio.get_earliest_sniff_timestamp() >= interval_end:
                yield frames_in_interval
                # Add frame to next interval use it to determine end of next interval
                frames_in_interval = [frame]
                interval_end = frame.wlan_radio.get_earliest_sniff_timestamp() + self.interval
            else:
                frames_in_interval.append(frame)

    def classify_interval_label(self, frames):
        features = self.extract_features_for_classification(frames)

        # Return the most common classification of all the frames as a single label(based on labels gained in training)
        # Returns an error if the model has not been fitted
        if features.size < 1:
            return None

        classifications = self.model.predict(features).tolist()
        return max(classifications, key=classifications.count)

    def classify_interval_confidence(self, frames):
        features = self.extract_features_for_classification(frames)

        if features.size < 1:
            return 0

        # Array of the probability for each label for each frame.
        prediction = self.model.predict_proba(features)

        # Summation of all frames.
        summation = prediction.sum(axis=0)

        # Returns the confidence for a given classification as a percentage.
        return max(summation) / np.sum(summation)

    def determine_device_classification(self, interval_classifications_with_confidence):
        classifications_with_high_confidence = list()
        threshold = 0.6

        # find all classifications with a confidence higher than 0.6
        for classification in interval_classifications_with_confidence:
            if classification[1] >= threshold:
                classifications_with_high_confidence.append(classification[0])
        if not classifications_with_high_confidence:
            return None
        # Returns the classification (label) with maximum occurrences
        return max(classifications_with_high_confidence, key=classifications_with_high_confidence.count)



    def labels_in_model(self):
        # Returns an array with the labels of the trained model.
        return self.model.classes_

    @staticmethod
    def _verify_item_is_frame(item):
        """
        This method raises an error if the given item is not a frame
        """
        if not isinstance(item, WifiFrame):
            raise ValueError('classify must be given generator that produces elements of type Frame')

    def train(self):

        labels = pd.read_csv("Data/new_labels.csv")
        files = self.get_file_paths()

        dfs = list()
        for file in files:
            dfs.append(frames_from_file_with_caching(file))
        df = pd.concat(dfs)

        cache_dataframe("Data/cache", 'unprocessed_training_data', df)

        # print("First for loop")
        # frames = []
        # for file_path in files:
        #     frames = chain_generators(map_to_frames(load_file(file_path), WifiCard("file", Point2D(0, 0))), frames)
        # devices = device_aggregator(frame_to_device_converter(frames), 50)
        #
        # print("Second for loop")
        # dfs = []
        # for device in devices:
        #     dfs.extend(list(map(lambda frame: frame.to_dataframe(), device.frames)))
        # df = pd.concat(dfs)
        #
        # print("Caching unprocessed training")
        # cache_dataframe("Data/cache", 'unprocessed_training_data', df)

        print("Processing")
        data, label_series = self.preprocess_data(df, labels)

        print("Split")
        input_train, input_test, labels_train, labels_test = train_test_split(data, label_series)

        print("Fitting")
        self.model.fit(input_train, labels_train)

        print("Report")
        res = classification_report(labels_test, self.model.predict(input_test))
        print(res)

        return res

    def extract_features_for_classification(self, frames):
        dfs = list()
        for item in frames:
            dfs.append(item.to_dataframe())
        df = pd.concat(dfs)
        df = self.drop_features(df)
        df['data_rate'] = df['data_rate'].fillna(0)
        df = df.dropna()
        return df

    def preprocess_data(self, df, labels):
        # Select rows that contain data from one of the devices with a label
        df = df[df['transmitter_address'].map(lambda x: labels.Address.str.contains(x).sum() == 1)]
        # Drop radio timestamp as it is NaN for the file data
        df = df.drop(['radio_timestamp'], axis='columns')
        # Create a series containing a label for each row

        df['data_rate'] = df['data_rate'].fillna(0)
        df = df.dropna()

        label_series = pd.DataFrame(df['transmitter_address']).set_index('transmitter_address').join(
            labels.set_index('Address')).squeeze()
        df = self.drop_features(df)

        return df, label_series

    @staticmethod
    def drop_features(df):
        # Drop radio timestamp as it is NaN for the file data
        df = df.drop(['radio_timestamp'], axis='columns', errors='ignore')
        # df['sniff_timestamp_0'] = pd.to_datetime(df['sniff_timestamp_0'],unit='s')
        df = df.drop(['receiver_address', 'transmitter_address'], axis='columns')
        # df['data_rate'] = df['data_rate'].fillna(0)
        return df

    @staticmethod
    def load_files(files):
        dfs = list()
        for file in files:
            dfs.append(frames_from_file_with_caching(file))

        return pd.concat(dfs)

    @staticmethod
    def get_file_paths():
        def add_path(folder):
            return lambda name: f'Data/{folder}/{name}'

        files = list()
        files.extend(list(map(add_path('Google Nest'),
                              ['dump1_2.4_ghz.pcapng', 'dump2_2.4_ghz.pcapng', 'dump1_5_ghz.pcapng',
                               'dump2_5_ghz.pcapng', 'dump3_5_ghz.pcapng', 'dump4_5_ghz.pcapng'])))
        files.extend(list(map(add_path('LittleElf'), ['dump.pcapng', 'dump1.pcapng', 'dump2.pcapng', 'dump3.pcapng'])))
        files.extend(list(map(add_path('Nikkei'), ['dump2.pcapng', 'dump3.pcapng', 'dump4.pcapng'])))
        files.extend(list(map(add_path('TP-Link'),
                              ['dump.pcapng', 'dump1.pcapng', 'dump2.pcapng', 'dump3.pcapng', 'dump4.pcapng',
                               'dump5.pcapng'])))
        files.extend(list(map(add_path('Blink'), ['dump1.pcapng', 'dump2.pcapng', 'dump4.pcapng'])))
        files.extend(list(map(add_path('Nedis'), ['dump.pcapng', 'dump1.pcapng', 'dump2.pcapng',
                                                  'dump3.pcapng', 'dump4.pcapng', 'dump5.pcapng'])))

        return files

    def save_model(self, filename):
        path_norm = os.path.normpath(f'Data/cache/savedModels/{filename}.joblib')
        dump(self.model, path_norm)

    def load_model(self, filename):
        path_norm = os.path.normpath(f'Data/cache/savedModels/{filename}.joblib')
        self.model = load(path_norm)
