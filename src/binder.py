"""Bindings class"""
import socket

class Bindings:
    """
    This class contains the communication functions.
    By extending this class, we will be able to support both simulator and raspberry communication.
    """

    def open_package_door(self):
        """Binding for activate servo motor and open the package door."""


class Server(Bindings):
    """
    Connects to the simulator via socket and sends the command to drop ball.
    """

    socket_client: socket.socket

    def __init__(self, host, port):

        try:
            self.socket_client = socket.socket()
            self.socket_client.connect((host, port))
        except socket.error as msg:
            print(f"Failed to connect server: {msg}")
            exit(0)

    def open_package_door(self):
        self.socket_client.send(b'\x01')


class File(Bindings):
    """
    Creates a message box instead sending commands to servo or simulator.
    """

    def __init__(self):
        pass


class Raspberry(Bindings):
    """
    Raspberry pi connector.
    """

    def __init__(self):
        pass