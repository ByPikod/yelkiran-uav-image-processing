import configparser
import os


def fill_config(conf: configparser.ConfigParser):
    """
    Fills the ConfigParser that passed as an argument with the default config variables.
    """
    conf["GENERAL"] = {
        "logging": True,
        "preview": True,
        "record": True,
        "camera-index": 1
    }

    conf["SIMULATOR"] = {
        "enabled": False,
        "host": "127.0.0.1",
        "port": 5710
    }


class ConfigUtil:
    """
    Config utils.
    """

    config_parser: configparser.ConfigParser

    def __init__(self, config_parser):
        self.config_parser = config_parser

    def get_string(self, locator: str) -> str | None:
        """
        Allows you to retrieve config data quickly.
        You can write "simulator.enabled" instead ["SIMULATOR"]["enabled"]
        """
        current_f = self.config_parser

        splitted_locator = locator.split(".")
        splitted_locator[0] = splitted_locator[0].upper()

        for next_f in splitted_locator:
            current_f = current_f[next_f]

        return current_f

    def get_bool(self, field: str) -> bool | None:
        """Returns bool data from config."""
        return self.get_string(field).lower() == "true"

    def get_int(self, field: str) -> int | None:
        """Returns int data from config."""
        try:
            return int(self.get_string(field))
        except ValueError:
            return 0


def get_config() -> ConfigUtil:
    """
    Prepares the ConfigParser and returns.
    """

    # Create a config
    conf = configparser.ConfigParser()

    # Fill with defalut variables
    fill_config(conf)

    # Read data
    root_dir = os.path.dirname(os.path.abspath(__file__))
    conf_path = os.path.join(root_dir, "configuration.ini")
    conf.read(conf_path)

    # Write data
    with open(conf_path, 'w') as conf_file:
        conf.write(conf_file)

    return ConfigUtil(conf)
