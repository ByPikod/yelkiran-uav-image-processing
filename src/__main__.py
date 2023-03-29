import logging
import config as conf

from server import Server
from bindings import Bindings
from processor import Processor

if __name__ == "__main__":

    # Configuration
    config = conf.get_config()

    # Logging
    if config.get_bool("general.logging"):
        logging.initialize("logs")

    binding: Bindings

    if config.get_bool("simulator.enabled"):
        # Try to connect server.
        print("Simulator enabled, trying to connect to the server.")
        binding = Server(config.get_string("simulator.host"), config.get_int("simulator.port")) 
    else:
        # There should be raspberry pi bindings.
        pass

    processor = Processor(binding, config)
