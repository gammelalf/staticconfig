import os.path
from typing import Dict, Any

import json


class ConfigError(RuntimeError):
    """An error while loading the config"""
    pass


class Namespace(dict):
    """
    A namespace is a python dict whose values can be accessed like attributes.

    It also ensures that its keys are identifier strings.
    The point is solely to have nicer syntax.
    """

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        if isinstance(key, str) and key.isidentifier():
            super().__setitem__(key, value)
        else:
            raise KeyError("Key must be identifier strings")


class Config(Namespace):
    """
    A namespace (dict) containing an applications config.

    The constructor takes no arguments and initialises all possible config options with some default values.

    How to use:
    - Use the classmethod `from_json` to load a json-formatted config file.
    - To add your own options just subclass this class and extends or overwrite the constructor.
    - Use `Namespace` objects to create sections.
    """

    def __init__(self):
        super().__init__()

    @classmethod
    def from_dict(cls, dct: Dict[str, Any]) -> "Config":
        """
        Create a config instance and load the values from a dict.

        :param dct: the config values
        :type dct: Dict[str, Any]
        :return: config instance
        :rtype: Config
        """
        config = cls()
        cls._update(config, dct)
        return config

    @classmethod
    def from_json(cls, config_file: str) -> "Config":
        """
        Load a json file and create a config instance from it.

        :param config_file: path to json file to load
        :type config_file: str
        :return: config instance
        :rtype: Config
        """
        if not os.path.exists(config_file):
            cls.to_json(cls(), config_file)
            raise ConfigError(config_file+" not found, generated template")
        with open(config_file) as f:
            dct = json.load(f)
        cls.config_path = config_file
        return cls.from_dict(dct)

    @classmethod
    def to_json(cls, config: "Config", config_file: str):
        """
        Dump a Config to a specified path as json.

        :param config: Existing Config object
        :type config: Config
        :param config_file: Path to json file
        :type config_file: str
        """
        with open(config_file, "w") as fh:
            json.dump(config, fh, indent=2, sort_keys=True)
            # Use sort keys to ensure deterministic config files

    @staticmethod
    def _update(dct, dct2):
        for key, value in dct2.items():
            if key not in dct:
                raise ConfigError("Unexpected config option: '"+key+"'")
            elif isinstance(value, dict):
                Config._update(dct[key], value)
            else:
                dct[key] = value
