from config import get_config
from server import Server
from bindings import Bindings
from processor import Processor

if __name__ == "__main__":

    config = get_config()

    binding: Bindings

    # Check if simulator enabled
    sim_conf = config["SIMULATOR"]
    simulator_enabled = sim_conf["enabled"].lower() == "true"

    if simulator_enabled:
        print("Simulator enabled, trying to connect to the server.")
        binding = Server(sim_conf["host"], int(sim_conf["port"]))  # Try to connect server.
    else:
        # There should be raspberry pi bindings.
        pass

    processor = Processor(binding, simulator_enabled)