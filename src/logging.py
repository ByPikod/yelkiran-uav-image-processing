import sys
import os

"""
This class saves prints into a log file.
"""


class CustomOut:

    def __init__(self, filename: str, std):
        self.console = std
        self.file = open(filename, 'w')

    def write(self, message):
        self.console.write(message)
        self.file.write(message)
        self.file.flush()
        os.fsync(self.file.fileno())

    def flush(self):
        self.console.flush()
        self.file.flush()
        os.fsync(self.file.fileno())


def initialize(directory):
    # Create directory if it doesn't exist.
    if not os.path.exists(directory):
        os.mkdir(directory)

    sys.stdout = CustomOut(os.path.join(directory, "stdout.txt"), sys.stdout)  # Stdout
    sys.stderr = CustomOut(os.path.join(directory, "stderr.txt"), sys.stderr)  # Stderr

    print("Logger initialized.")
