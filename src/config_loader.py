import yaml
from jsonschema import validate
import shutil

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


def load_config(config_file):
    """
    Loads the configuration yml file, validates if with json schema and returns the config object
    :param config_file: path to the config file
    :return: config object
    """
    try:
        with open(config_file, 'r') as stream:
            config = yaml.safe_load(stream)
    except FileNotFoundError:
        print("Config file not found, copying default config file")

        shutil.copy(f"{config_file}.default", config_file)
        with open(config_file, 'r') as stream:
            config = yaml.safe_load(stream)

    validate(config, schema)

    return config
