import yaml
from config.models import Config
from config.validator import validate_config


def load_config(file_path="apis.yaml"):
    try:
        with open(file_path, "r") as file:
            raw = yaml.safe_load(file)

        validate_config(raw)

        return Config(raw)

    except FileNotFoundError:
        raise Exception(f"Config file not found: {file_path}")

    except yaml.YAMLError as e:
        raise Exception(f"YAML parsing error: {e}")