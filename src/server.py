import socket

from bindings import Bindings


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
