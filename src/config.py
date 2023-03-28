import configparser
import os

"""
Fills the ConfigParser that passed as an argument with the default config variables.
"""


def fill_config(conf: configparser.ConfigParser):

    conf["SIMULATOR"] = {
        "enabled": False,
        "host": "127.0.0.1",
        "port": 5710
    }


"""
Prepares the ConfigParser and returns.
"""


def get_config() -> configparser.ConfigParser:

    # Create a config
    conf = configparser.ConfigParser()

    # Put default variables
    fill_config(conf)

    # Read config from file
    root_dir = os.path.dirname(os.path.abspath(__file__))
    conf_path = os.path.join(root_dir, "configuration.ini")
    conf.read(conf_path)

    # Write file (that creates a config if there is not)
    with open(conf_path, 'w') as conf_file:
        conf.write(conf_file)

    return conf
