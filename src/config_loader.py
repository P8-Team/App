import shutil
from os import path

import yaml
from jsonschema import validate

schema = {
    "type": "object",
    "required": ["adapters"],
    "properties": {
        "adapters": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "required": ["location"],
                "properties": {
                    "location": {
                        "type": "array",
                        "items": {
                            "type": "number",
                        },
                        "minItems": 2,
                        "maxItems": 2,
                    }
                }
            }
        },
        "hard_data_file": {
            "type": "string"
        },
        "labels_file": {
            "type": "string"
        },
        "saved_models_folder": {
            "type": "string"
        },
        "cache_folder": {
            "type": "string"
        },
        "classifier_interval": {
            "type": "number"
        },
        "device_buffer_size": {
            "type": "number"
        },
        "classifier_train_split": {
            "type": "number"
        },
        "path_loss_exponent": {
            "type": "number"
        },
        "confidence_threshold": {
            "type": "number"
        },
        "training_files": {
            "type": "object",
            "additionalProperties": {
                "type": "array"
            }
        },
        "transmission_power_placeholder_2ghz": {
            "type": "number"
        },
        "transmission_power_placeholder_5ghz": {
            "type": "number"
        }
    }
}


def load_config_file(file_path):
    if not path.exists(file_path):
        print("Config file not found, copying default config file")
        shutil.copy(f"{file_path}.default", file_path)

    with open(file_path, 'r') as stream:
        return load_config(stream)


def load_config(config_stream):
    """
    Loads the configuration yml file, validates it with json schema and returns the config object
    :param config_stream: stream containing data from config file
    :return: config object
    """
    config = yaml.safe_load(config_stream)
    validate(config, schema)

    return config
