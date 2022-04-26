import pandas as pd
from src.classifier import Classifier
from src.wifi.wifi_card import WifiCard
from src.wifi.wifi_frame import WifiFrame
from test.utils.wifi_frame_factory import frame_factory
from test.utils.wifi_test_utils import Frame, Layer
from sympy import Point2D


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


def test_classify():
    cl = Classifier(1)
    frames = [frame_factory(1), frame_factory(2), frame_factory(2), frame_factory(2), frame_factory(3),
              frame_factory(3), frame_factory(6)]
    frames_db = pd.DataFrame
    for frame in frames:
        frames_db.append(frame.to_dataframe())
    assert cl.classify(frames) is not None


def test_classifier_has_labels():
    cl = Classifier(1)
    frames = [frame_factory(1), frame_factory(2), frame_factory(2), frame_factory(2), frame_factory(3),
              frame_factory(3), frame_factory(6)]
    frames_db = pd.DataFrame
    for frame in frames:
        frames_db.append(frame.to_dataframe())
    labels = pd.DataFrame.from_dict({'Address': ["00:00:00:00:00:01"], 'Label': ['test']})

    assert cl.labels_in_model() is list
    assert len(cl.labels_in_model()) > 0
    assert cl.labels_in_model()[0] is 'test'


def test_classify_returns_label():
    cl = Classifier(1)
    #cl.train find alternativ
    possible_label_list = cl.labels_in_model()
    assert cl.classify_interval_label() in possible_label_list


def test_classify_return_confidence():
    cl = Classifier(1)
    #cl.train find alternativ
    assert 0 <= cl.classify_interval_confidence() <= 1
