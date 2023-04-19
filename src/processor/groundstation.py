"""Groundstation connection"""
import pickle
import socket as s
import threading
import time

import cv2


class Groundstation:
    """
    This class establishes the connection between groundstation and raspberry pi.
    """

    tcp_socket: s.socket
    udp_socket: s.socket

    query_addr: tuple[str, int]
    stream_addr: tuple[str, int]

    running: bool = True     # This will terminate connection loop if False
    connected: bool = False  # This will prevent stream through UDP if False
    next_try: int = 0

    def __init__(self, host: str, query_port: int, stream_port: int) -> None:
        self.query_addr = (host, query_port)
        self.stream_addr = (host, stream_port)
        self.thread = threading.Thread(target=self.initialize_conn)
        self.thread.start()

    def initialize_conn(self) -> None:
        """
        Re-establish connection everytime connection is broken and receive messages.
        """
        while self.running:

            # Connect server
            self.tcp_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
            try:
                self.tcp_socket.connect(self.query_addr)
            except Exception as e:
                print(f"Failed to connect groundstation: {e}")
                print(f"Trying again in 3 seconds...")
                self.tcp_socket.close()
                time.sleep(3)
                continue

            # Successfully connected
            self.on_tcp_established()
            # Listen server
            self.listen_tcp()
            # Connection terminated due to an error.
            self.on_tcp_terminated()
            print()

    def terminate(self):
        self.running = False
        self.connected = False
        self.tcp_socket.close()
        self.udp_socket.close()

    def listen_tcp(self) -> None:
        """
        Listen for TCP messages.
        """

        while self.running:

            data: bytes = b''
            try:
                data = self.tcp_socket.recv(1024)
            except Exception as e:
                self.tcp_socket.close()
                print(f"Unable to maintain ground station connection: {e}")
                print("Trying to re-establish connection in 3 seconds.")
                time.sleep(3)
                break

            self.on_tcp_message(data)

    def send_udp_message(self, frame) -> None:
        """
        Stream frame to the groundstation.
        :param frame: Frame
        """

        # Cooldown & connection check
        if self.next_try > time.time() or not self.connected:
            return

        # Convert to byte array
        encoded, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
        data = pickle.dumps(buffer)

        # Stream
        try:
            self.udp_socket.sendto(data, self.stream_addr)
        except OSError:
            if not self.connected:
                return
            self.next_try = int(time.time()) + 1000
            print("Failed to stream output to groundstation. Trying again.")

    def on_tcp_message(self, data: bytes) -> None:
        """
        Triggered when a packet is caught.
        :param data: Packet
        """
        pass

    def on_tcp_established(self) -> None:
        """
        Triggered when tcp connection is established.
        """

        self.udp_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.connected = True
        print("Connection with the ground station has successfully established!")

    def on_tcp_terminated(self) -> None:
        """
        Triggered when tcp connection is broken.
        """

        self.connected = False
        self.udp_socket.close()
