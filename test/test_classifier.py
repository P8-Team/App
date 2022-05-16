import os
import os.path

import pandas as pd
import pytest
from sympy import Point2D

from src.classifier import Classifier
from src.device.device import Device
from src.wifi.wifi_card import WifiCard
from src.wifi.wifi_frame import WifiFrame
from test.utils.wifi_frame_factory import frame_factory
from test.utils.wifi_test_utils import Frame, Layer

test_config_1 = {'hard_data_file': 'Data/hard_data.csv',
                 'classifier_interval': 1,
                 'confidence_threshold': 0.6,
                 'labels_file': 'Data/new_labels.csv',
                 'saved_models_folder': 'Data/cache/savedModels/',
                 'training_files': {'Google Nest': ['file1', 'file2', 'file3']}}

test_config_2 = {'hard_data_file': 'Data/hard_data.csv',
                 'classifier_interval': 2,
                 'confidence_threshold': 0.6,
                 'labels_file': 'Data/new_labels.csv',
                 'saved_models_folder': 'Data/cache/savedModels/',
                 'training_files': {'Google Nest': ['file1', 'file2', 'file3']}}


def test_get_file_paths_returns_list_of_strings():
    classifier = Classifier(test_config_1)
    file_paths = classifier.get_file_paths()
    assert all(isinstance(x, str) for x in file_paths) is True
    assert file_paths[0] == 'Data/Google Nest/file1.pcapng'
    assert file_paths[2] == 'Data/Google Nest/file3.pcapng'


def test_preprocess_data():
    frame = Frame("340", "1647417907.513663000", {
        'wlan': Layer({
            'fcs': '0x1234',
            'wlan.fc.type': '0',
            'wlan.fc.subtype': '4',
            'wlan.ra_resolved': '00:0c:29:b7:d9:b0',
            'wlan.ta_resolved': '00:0c:29:b7:d9:b1',
        }),
        'wlan_radio': Layer({
            'wlan_radio.signal_dbm': '-62',
            'wlan_radio.data_rate': '54',
            'wlan_radio.timestamp': '1567757308'
        })
    })

    wifi_frame = WifiFrame.from_frame(frame, WifiCard("wlan0", Point2D(0, 0)))
    wifi_frame.wlan_radio.signals[0].timestamp_delta = 10
    wifi_frame.wlan_radio.frequency_mhz = 2
    labels = pd.DataFrame.from_dict({'Address': ["00:0c:29:b7:d9:b1"], 'Label': ['test']})

    classifier = Classifier(test_config_1)

    result_df, result_labels = classifier.preprocess_data(wifi_frame.to_dataframe(), labels)

    assert result_labels == "test"
    assert len(result_df.columns) == 6


def test_classifier_drops_features():
    classifier = Classifier(test_config_1)
    frames_db = frame_factory(1).to_dataframe()
    for i in range(1, 20):
        frames_db = pd.concat([frames_db, frame_factory(i).to_dataframe()], axis=0)
    new_frames_db = classifier.drop_features(frames_db)

    dropped_columns = {'radio_timestamp', 'receiver_address', 'transmitter_address'}

    assert dropped_columns.issubset(frames_db.columns) is True
    for column in dropped_columns:
        assert {column}.issubset(new_frames_db) is False


@pytest.fixture
def cl():
    classifier = Classifier(test_config_1)

    frames_df = frame_factory(1).to_dataframe()
    for i in range(1, 20):
        frames_df = pd.concat([frames_df, frame_factory(i).to_dataframe()], axis=0)

    labels = pd.DataFrame.from_dict({'Address': ["00:00:00:00:00:01"], 'Label': ['test']})
    training_data, label_series = classifier.preprocess_data(frames_df, labels)

    classifier.model.fit(training_data, label_series)
    return classifier


def test_classifier_has_labels(cl):
    assert cl.labels_in_model()[0] == 'test'


def test_classifier_return_confidence_for_interval(cl):
    frames = []
    for i in range(0, 10):
        frames.append(frame_factory(i))
    assert 0 <= cl.classify_interval_confidence(frames) <= 1


def test_classifier_return_most_frequent_label_with_high_confidence(cl):
    assert cl.determine_device_classification(
        [['Nedis', 0.6], ['test', 0.7], ['test', 0.8], ['Nedis', 0.2], ['Nedis', 0.5]]) == 'test'


def generator(items: list):
    for item in items:
        yield item


def test_classifier_returns_device():
    classifier = Classifier(test_config_1)

    frames_db = frame_factory(1).to_dataframe()
    for i in range(1, 20):
        frames_db = pd.concat([frames_db, frame_factory(i).to_dataframe()], axis=0)

    labels = pd.DataFrame.from_dict({'Address': ["00:00:00:00:00:01"], 'Label': ['Nikkei']})
    training_data, label_series = classifier.preprocess_data(frames_db, labels)

    classifier.model.fit(training_data, label_series)

    device = Device("00:00:00:00:00:01", [
        frame_factory(1), frame_factory(2),
    ])

    result = list(classifier.classify([device]))
    assert result[0] == device


def test_classifier_accumulate_frames():
    classifier = Classifier(test_config_2)
    frame_gen = generator([frame_factory(0), frame_factory(0.5), frame_factory(1), frame_factory(1.9),
                           frame_factory(2), frame_factory(2.1), frame_factory(2.5), frame_factory(3)])
    accumulated_frames = next(classifier.accumulate_frames(frame_gen))
    for e in accumulated_frames:
        assert isinstance(e, WifiFrame)
    assert len(accumulated_frames) == 4


def test_classifier_save_and_load_model(cl):
    filename = 'testSave'
    path_norm = os.path.normpath('Data/cache/savedModels/{}.joblib'.format(filename))
    if os.path.exists(path_norm):
        os.remove(path_norm)
    cl.save_model(filename)
    assert os.path.exists(path_norm) is True

    cl.model = None
    cl.load_model(filename)
    assert cl.model is not None


@pytest.fixture
def frames():
    frames = []
    for i in range(1, 20):
        frames.append(frame_factory(i))
    return frames


def test_classifier_extract_correct_features(cl, frames):
    extracted_features = cl.extract_features_for_classification(frames)

    assert isinstance(extracted_features, pd.DataFrame) is True
    assert len(extracted_features.columns.values.tolist()) > 0

    extracted_features = extracted_features.columns.values.tolist()
    labels_from_training = cl.labels_in_model().tolist()

    for label in labels_from_training:
        assert extracted_features.__contains__(label) is False


def test_classifier_extracting_same_features_ignoring_labels(frames):
    classifier = Classifier(test_config_1)

    frames_df = frame_factory(1).to_dataframe()
    for i in range(2, 20):
        frames_df = pd.concat([frames_df, frame_factory(i).to_dataframe()], axis=0)

    labels = pd.DataFrame.from_dict({'Address': ["00:00:00:00:00:01"], 'Label': ['test']})
    training_data, label_series = classifier.preprocess_data(frames_df, labels)

    features_classifier = classifier.extract_features_for_classification(frames).columns.values.tolist()
    features_training = training_data.columns.values.tolist()

    assert len(features_training) > 0
    assert features_classifier == features_training


def test_classifier_returns_label_for_interval(cl, frames):
    possible_labels_list = cl.labels_in_model()
    assert cl.classify_interval_label(frames) in possible_labels_list


def test_classifier_return_confidence_for_interval(cl, frames):
    assert 0 <= cl.classify_interval_confidence(frames) <= 1
