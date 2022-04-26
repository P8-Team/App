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
    Loads the configuration yml file, validates if with json schema and returns the config object
    :param config_stream: stream containing data from config file
    :return: config object
    """
    config = yaml.safe_load(config_stream)
    validate(config, schema)

    return config