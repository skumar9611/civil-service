"""The config script.
This script reads the config.json and converts it to a JSON.
"""

import json
import os

CONFIG_PATH = os.path.join(os.getcwd(), 'config.json')


def read_configuration():
    """
    Method to read the config file
    :return dict: The configuration dictionary.
    """
    try:
        with open(CONFIG_PATH, "r") as reader:
            configuration = json.loads(reader.read())

        config_keys = configuration.keys()
        for config_key in config_keys:
            if config_key.upper() in os.environ.keys():
                # Use the config properties if it is defined in env variables
                configuration[config_key] = os.environ[config_key.upper()]
        return configuration

    except Exception as e:
        return "Error in config file. ERROR:{}".format(e)


config = read_configuration()
