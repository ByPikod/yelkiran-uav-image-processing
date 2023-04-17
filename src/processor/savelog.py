"""Logging"""
import sys
import os
import datetime


class CustomOut:
    """
    This class saves prints into a log file.
    """

    def __init__(self, filename: str, std, format_msg=False) -> None:
        self.console = std
        self.file = open(filename, 'w')
        self.format_msg = format_msg

    def write(self, message) -> None:
        """
        Write override.
        :param message: Message to print
        """
        if self.format_msg and message != "\n":
            message = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}"
            
        self.console.write(message)
        
        # Write logs
        self.file.write(message)
        self.file.flush()
        os.fsync(self.file.fileno())

    def flush(self) -> None:
        """
        Flush I/O
        """
        self.console.flush()
        self.file.flush()
        os.fsync(self.file.fileno())


def initialize(directory: str) -> None:
    """
    Initialize logging system.
    :param directory: Directory to save stdout.txt and stderr.txt
    """
    # Create directory if it doesn't exist.
    if not os.path.exists(directory):
        os.mkdir(directory)

    sys.stdout = CustomOut(os.path.join(directory, "stdout.txt"), sys.stdout, True)  # Stdout
    sys.stderr = CustomOut(os.path.join(directory, "stderr.txt"), sys.stderr)  # Stderr

    print("Logger initialized.")
