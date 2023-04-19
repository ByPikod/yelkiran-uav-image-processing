"""Configuration management."""
import configparser
import os


class ConfigUtil:
    """
    Config utils.
    """

    config_parser: configparser.ConfigParser

    @staticmethod
    def fill_config(conf: configparser.ConfigParser) -> None:
        """
        Fills the ConfigParser that passed as an argument with the default config variables.
        :param conf: Config to fill
        """

        conf["GENERAL"] = {
            "record": True,
            "logging": True,
            "preview": True,
            "visualize-processing": True,
            "record-dir": "./",
            "video-source": "simulator",
            "camera-index": 1
        }

        conf["OPENCV"] = {
            "upper_h": 180,
            "upper_s": 255,
            "upper_v": 255,
            "lower_h": 0,
            "lower_s": 0,
            "lower_v": 0,
            "collision-box-width": 100,
            "collision-box-height": 100,
            "collision-box-horizontal-offset": 0,
            "collision-box-vertical-offset": 0,
        }

        conf["GROUNDSTATION"] = {
            "enabled": True,
            "host": "127.0.0.1",
            "query_port": 1864,
            "stream_port": 2023
        }

        conf["FILE"] = {
            "video-path": "source.mp4"
        }

        conf["SIMULATOR"] = {
            "host": "127.0.0.1",
            "port": 5710
        }

    def __init__(self) -> None:

        # Create a config
        self.config_parser = configparser.ConfigParser()

        # Fill with default variables
        self.fill_config(self.config_parser)

        # Read data
        root_dir = os.path.dirname(os.path.abspath(__file__))
        self.conf_path = os.path.join(root_dir, "configuration.ini")
        self.config_parser.read(self.conf_path)

        # Write data
        self.save()

    def get_string(self, locator: str) -> str:
        """
        Allows you to retrieve config data quickly.
        :param locator: Example locator: "simulator.enabled"
        :return: Matching data
        """

        split_locator = locator.split(".")
        split_locator[0] = split_locator[0].upper()

        return self.config_parser[split_locator[0]][split_locator[1]]

    def get_bool(self, field: str) -> bool:
        """
        Returns bool data from config.
        :param field: Locator
        :return: Matching boolean data
        """

        return self.get_string(field).lower() == "true"

    def get_int(self, field: str) -> int:
        """
        Returns int data from config.
        :param field: Locator
        :return: Matching integer data
        """

        try:
            return int(self.get_string(field))
        except ValueError:
            return 0

    def set_field(self, locator: str, value: any) -> None:
        """
        Allows you to set config data quickly.
        :param locator: Where to set
        :param value: Value to set
        """

        split_locator = locator.split(".")
        split_locator[0] = split_locator[0].upper()

        self.config_parser[split_locator[0]][split_locator[1]] = value

    def save(self) -> None:
        """
        Save config.
        """

        with open(self.conf_path, 'w') as conf_file:
            self.config_parser.write(conf_file)
