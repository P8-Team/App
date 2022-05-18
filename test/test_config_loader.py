from unittest import mock

import pytest
import yaml
from jsonschema.exceptions import ValidationError

from src.config_loader import load_config, load_config_file


def test_config_loader_invalid_type():
    data = yaml.dump(
        {"adapters": {"wlan1": {"location": [0]}},
         "hard_data_file": "string",
         "labels_file": "string",
         "classifier_interval": 3,
         "device_buffer_size": 3,
         "path_loss_exponent": 2,
         "confidence_threshold": 0.5,
         "saved_models_folder": "string"})

    with pytest.raises(ValidationError):
        load_config(data)


def test_config_loader_returns_valid_config():
    data = yaml.dump(
        {"adapters": {"wlan1": {"location": [0, 0.433]}},
         "hard_data_file": "string",
         "labels_file": "string",
         "classifier_interval": 3,
         "device_buffer_size": 3,
         "path_loss_exponent": 2,
         "confidence_threshold": 0.5,
         "saved_models_folder": "Somewhere",
         "training_files": {"Google Nest": ["file1", "file2", "file3"]}})

    config = load_config(data)
    assert config ==  {"adapters": {"wlan1": {"location": [0, 0.433]}},
         "hard_data_file": "string",
         "labels_file": "string",
         "classifier_interval": 3,
         "device_buffer_size": 3,
         "path_loss_exponent": 2,
         "confidence_threshold": 0.5,
         "saved_models_folder": "Somewhere",
         "training_files": {"Google Nest": ["file1", "file2", "file3"]}}


def test_load_config_file_copies_default():
    with mock.patch('os.path.exists', return_value=False):
        with mock.patch('shutil.copy') as mock_copy:
            with mock.patch('builtins.open', mock.mock_open(read_data=""), create=True):
                with mock.patch('src.config_loader.load_config', return_value={}) as mock_load:
                    load_config_file('config.yaml')
                    mock_copy.assert_called_once_with('config.yaml.default', 'config.yaml')
                    mock_load.assert_called()


def test_load_config_file_returns_config():
    with mock.patch('os.path.exists', return_value=True):
        with mock.patch('builtins.open', mock.mock_open(read_data="")):
            with mock.patch('src.config_loader.load_config', return_value={}) as mock_load:
                load_config_file('config.yaml')
                mock_load.assert_called()
