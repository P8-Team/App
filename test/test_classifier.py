import pandas as pd
import pytest
from src.classifier import Classifier
from src.wifi.wifi_card import WifiCard
from src.wifi.wifi_frame import WifiFrame
from test.utils.wifi_frame_factory import frame_factory
from test.utils.wifi_test_utils import Frame, Layer
from sympy import Point2D
import os


def test_get_file_paths_returns_list_of_strings():
    classifier = Classifier(1)
    assert all(isinstance(x, str) for x in classifier.get_file_paths()) == True


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
    labels = pd.DataFrame.from_dict({'Address': ["00:0c:29:b7:d9:b1"], 'Label': ['test']})

    classifier = Classifier(1)

    result_df, result_labels = classifier.preprocess_data(wifi_frame.to_dataframe(), labels)

    assert result_labels == "test"
    assert len(result_df.columns) == 7


def test_classifier_drops_features():
    cl = Classifier(1)
    frames_db = frame_factory(1).to_dataframe()
    for i in range(1, 20):
        frames_db = pd.concat([frames_db, frame_factory(i).to_dataframe()], axis=0)
    new_frames_db = cl.drop_features(frames_db)

    dropped_columns = {'radio_timestamp', 'receiver_address', 'transmitter_address'}

    assert dropped_columns.issubset(frames_db.columns) == True
    for column in dropped_columns:
        assert {column}.issubset(new_frames_db) == False


def test_classifier_correct_null_values():
    cl = Classifier(1)
    frames_db = frame_factory(1).to_dataframe()
    for i in range(1, 20):
        frames_db = pd.concat([frames_db, frame_factory(i).to_dataframe()], axis=0)
    new_frames_db = cl.drop_features(frames_db)

    assert {'data_rate'}.issubset(new_frames_db.columns) == True
    assert frames_db['data_rate'].isnull().values.any() == True
    for i, e in enumerate(frames_db['data_rate'].values.tolist()):
        if e == None:
            assert new_frames_db['data_rate'].values.tolist()[i] == 0


@pytest.fixture
def cl():
    cl = Classifier(2)

    frames_df = frame_factory(1).to_dataframe()
    for i in range(1, 20):
        frames_df = pd.concat([frames_df, frame_factory(i).to_dataframe()], axis=0)

    labels = pd.DataFrame.from_dict({'Address': ["00:00:00:00:00:01"], 'Label': ['test']})
    training_data, label_series = cl.preprocess_data(frames_df, labels)

    cl.model.fit(training_data, label_series)
    return cl


def test_classifier_has_labels(cl):
    assert cl.labels_in_model()[0] == 'test'


def generator(items: list):
    for item in items:
        yield item


def test_classifier_accumulate_frames():
    cl = Classifier(2)
    frame_gen = generator([frame_factory(0), frame_factory(0.5), frame_factory(1), frame_factory(1.9),
                           frame_factory(2), frame_factory(2.1), frame_factory(2.5), frame_factory(3)])
    accumulated_frames = next(cl.accumulate_frames(frame_gen))
    for e in accumulated_frames:
        assert isinstance(e, WifiFrame)
    assert len(accumulated_frames) == 4


def test_classifier_returns_label_for_classify(cl):
    frame_gen = generator([frame_factory(1), frame_factory(2), frame_factory(3), frame_factory(4)])
    possible_labels_list = cl.labels_in_model()
    assert next(cl.classify(frame_gen)) in possible_labels_list


@pytest.fixture
def frames():
    frames = []
    for i in range(1, 20):
        frames.append(frame_factory(i))
    return frames


def test_classifier_extract_correct_features(cl, frames):
    extracted_features = cl.extract_features_for_classification(frames)

    assert isinstance(extracted_features, pd.DataFrame) == True
    assert len(extracted_features.columns.values.tolist()) > 0

    extracted_features = extracted_features.columns.values.tolist()
    labels_from_training = cl.labels_in_model().tolist()

    for label in labels_from_training:
        assert extracted_features.__contains__(label) is False


def test_classifier_extracting_same_features_ignoring_labels(frames):
    cl = Classifier(1)

    frames_df = frame_factory(1).to_dataframe()
    for i in range(2, 20):
        frames_df = pd.concat([frames_df, frame_factory(i).to_dataframe()], axis=0)

    labels = pd.DataFrame.from_dict({'Address': ["00:00:00:00:00:01"], 'Label': ['test']})
    training_data, label_series = cl.preprocess_data(frames_df, labels)

    features_classifier = cl.extract_features_for_classification(frames).columns.values.tolist()
    features_training = training_data.columns.values.tolist()

    assert len(features_training) > 0
    assert features_classifier == features_training


def test_classifier_returns_label_for_interval(cl, frames):
    possible_labels_list = cl.labels_in_model()
    assert cl.classify_interval_label(frames) in possible_labels_list


def test_classifier_return_confidence_for_interval(cl, frames):
    assert 0 <= cl.classify_interval_confidence(frames) <= 1

