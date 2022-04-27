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


def test_classifier_load_files():
    cl = Classifier(1)
    test_path = os.path.normpath('test/test_data/LittleFairy.pcapng')
    # TODO: Don't forget
    assert False


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
    frames_db_new = cl.drop_features(frames_db)

    dropped_columns = {'radio_timestamp', 'receiver_address', 'transmitter_address'}

    assert dropped_columns.issubset(frames_db.columns) == True
    for column in dropped_columns:
        assert {column}.issubset(frames_db_new) == False
    assert {'data_rate'}.issubset(frames_db_new.columns) == True
    assert frames_db['data_rate'].isnull().values.any() == True
    assert frames_db_new['data_rate'].isnull().values.any() == False


def test_classifier_accumulate_frames():
    assert False


@pytest.fixture
def cl():
    cl = Classifier(1)

    frames_db = frame_factory(1).to_dataframe()
    for i in range(1, 20):
        frames_db = pd.concat([frames_db, frame_factory(i).to_dataframe()], axis=0)

    labels = pd.DataFrame.from_dict({'Address': ["00:00:00:00:00:01"], 'Label': ['test']})
    training_data, label_series = cl.preprocess_data(frames_db, labels)

    cl.model.fit(training_data, label_series)
    return cl


def test_classifier_has_labels(cl):
    assert cl.labels_in_model()[0] == 'test'


def generator(items: list):
    for item in items:
        yield item


def test_classifier_returns_label_for_classify(cl):
    frame_gen = generator([frame_factory(1), frame_factory(2)])
    possible_labels_list = cl.labels_in_model()
    assert next(cl.classify(frame_gen)) in possible_labels_list


@pytest.fixture
def frames():
    frames = []
    for i in range(0, 10):
        frames.append(frame_factory(i))
    return frames


def test_classifier_extract_features(cl, frames):
    extracted_features = cl.extract_features_for_classification(frames)
    assert isinstance(extracted_features, pd.DataFrame) == True
    assert {'Label'}.issubset(extracted_features.columns) == False


def test_classifier_extracting_same_features_ignoring_labels(cl, frames):
    features_classification = cl.extract_features_for_classification(frames)
    frame_df = frames[0].to_dataframe()
    for frame in frames[1:]:
        frame_df = pd.concat([frame_df, frame.to_dataframe()], axis=0)
    features_training, training_labels = cl.preprocess_data(frame_df)

    features_training.columns.to_dict

    assert features_training.columns.values.issubset(features_classification.columns) == True

    #classification_columns_list = features_classification.columns.values.tolist()
    #training_columns_list = features_training.columns.values.tolist()

    # assert dropped_columns.issubset(frames_db.columns) == True
    # Get all columns from class features
    # Assert they are subset of train features
    # Assert train features has 1 more coloumn
    # Assert that coloumn is labels.

def test_classifier_returns_label_for_interval(cl, frames):
    possible_labels_list = cl.labels_in_model()
    assert cl.classify_interval_label(frames) in possible_labels_list


def test_classifier_return_confidence_for_interval(cl, frames):
    assert 0 <= cl.classify_interval_confidence(frames) <= 1









