"""Logging"""
import sys
import os


class CustomOut:
    """
    This class saves prints into a log file.
    """

    def __init__(self, filename: str, std):
        self.console = std
        self.file = open(filename, 'w')

    def write(self, message):
        """Write override."""
        self.console.write(message)
        self.file.write(message)
        self.file.flush()
        os.fsync(self.file.fileno())

    def flush(self):
        """Flush override."""
        self.console.flush()
        self.file.flush()
        os.fsync(self.file.fileno())


def initialize(directory: str) -> None:
    """ Standard output goes to log file after logging initialized. """
    # Create directory if it doesn't exist.
    if not os.path.exists(directory):
        os.mkdir(directory)

    sys.stdout = CustomOut(os.path.join(directory, "stdout.txt"), sys.stdout)  # Stdout
    sys.stderr = CustomOut(os.path.join(directory, "stderr.txt"), sys.stderr)  # Stderr

    print("Logger initialized.")
