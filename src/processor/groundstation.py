"""Groundstation connection"""
import pickle
import socket as s
import time

import cv2


class Groundstation:
    """
    This class establishes the connection between groundstation and raspberry pi.
    """

    socket: s.socket
    next_try: int

    def __init__(self, addr: tuple[str, int]) -> None:
        self.addr = addr
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.next_try = 0

    def stream(self, frame) -> None:
        """
        Stream frame to the groundstation.
        :param frame: Frame
        """
        
        # Cooldown for trying again.
        if self.next_try > time.time():
            return

        # Convert to byte array
        encoded, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
        data = pickle.dumps(buffer)

        # Stream
        try:
            self.socket.sendto(data, self.addr)
        except OSError:
            self.next_try = int(time.time()) + 1000
            print("Failed to stream output to groundstation. Trying again.")
