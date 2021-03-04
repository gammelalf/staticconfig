import os.path
from typing import Dict, Any

import json


class ConfigError(RuntimeError):
    """An error while loading the config"""
    pass


class Namespace(dict):
    """
    A namespace is a python dict whose values can be accessed like attributes.
    It ensures that its keys are identifier strings.
    When an uninitialised key is accessed, it will be initialised with a new empty Namespace object.

    The point is solely to have nicer syntax.
    """

    def __getattr__(self, key):
        return self.setdefault(key, Namespace())

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError("Key must be string")
        elif not key.isidentifier():
            raise ValueError("Key must be valid identifier")
        else:
            super().__setitem__(key, value)


class Config(Namespace):
    """
    A namespace (dict) containing an applications config.

    The constructor takes no arguments and initialises all possible config options with some default values.

    How to use:
    - Use the classmethod `from_json` to load a json-formatted config file.
    - To add your own options just subclass this class and extends or overwrite the constructor.
    - Use `Namespace` objects to create sections.
    """

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
        If the specified file doesn't exists create one and quit the program.

        :param config_file: path to json file to load
        :type config_file: str
        :return: config instance
        :rtype: Config
        """
        if not os.path.exists(config_file):
            config = cls()
            config.to_json(config_file)
            config.quit(config_file+" not found, generated template")

            # This return is only reached when quit is overwritten in subclass
            return config

        else:
            with open(config_file) as f:
                dct = json.load(f)
            return cls.from_dict(dct)

    def to_json(self, config_file: str) -> None:
        """
        Dump a Config to a specified path as json.

        :param config_file: Path to json file
        :type config_file: str
        """
        with open(config_file, "w") as fh:
            # Use sort keys to ensure deterministic config files
            json.dump(self, fh, indent=2, sort_keys=True)

    @staticmethod
    def _update(dct: dict, dct2: dict) -> None:
        """
        Update a dictionary recursively

        :param dct: dictionary to update
        :type dct: dict
        :param dct2: dictionary providing the new data
        :type dct2: dict
        """
        for key, value in dct2.items():
            if key not in dct:
                raise ConfigError("Unexpected config option: '"+key+"'")
            elif isinstance(value, dict):
                Config._update(dct[key], value)
            else:
                dct[key] = value

    @staticmethod
    def quit(msg: str) -> None:
        """
        This function is called after a new config file has being created.
        It stops the program, because the user should first have a look and the config before proceeding.

        It can be overwritten in subclasses for custom behaviour.
        :param msg: A message to print before quitting
        :type msg: string
        """
        print(msg)
        quit(0)
