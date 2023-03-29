"""Image processing."""
import datetime
import os

import logging
import window
import config as conf

from server import Server
from bindings import Bindings

import cv2
import numpy as np


class Processor:
    """
    Processor going to call bindings according to processed video.
    """

    bindings: Bindings
    config: conf.ConfigUtil

    preview: bool
    record: bool

    result: cv2.VideoWriter
    capture: cv2.VideoCapture

    def __init__(self):

        # Configuration
        config = conf.ConfigUtil()

        # Unique folder
        self.record_dir = f"recording {datetime.datetime.now().strftime('%d.%m.%Y %H-%M-%S')}"

        # Logging
        if config.get_bool("general.logging"):
            logging.initialize(self.record_dir)

        # Bindings

        if not config.get_bool("simulator.enabled"):
            # There should be raspberry pi bindings.
            pass
        else:
            # Try to connect server.
            print("Simulator enabled, trying to connect to the server.")
            self.binding = Server(config.get_string("simulator.host"), config.get_int("simulator.port"))

        self.config = config
        self.preview = self.config.get_bool("general.preview")
        self.record = self.config.get_bool("general.record")

        try:
            self.start_loop()
        except cv2.error as err:
            print(f"An error has occurred while processing video camera: \n{err}")

    def get_capture_size(self) -> tuple[int, int]:
        """Returns the size of the capture."""
        frame_width = int(self.capture.get(3))
        frame_height = int(self.capture.get(4))
        return frame_width, frame_height


    def start_loop(self) -> None:
        """Main loop for image processing."""

        # Get webcam capture
        self.capture = cv2.VideoCapture(self.config.get_int("general.camera-index"))

        # Fix size for simulator.
        if self.config.get_bool("simulator.enabled"):
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Create recording if enabled.
        video_path = os.path.join(self.record_dir, "video.avi")
        if self.record:
            size = self.get_capture_size()
            self.result = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'XVID'), 30, size)

        # Name window
        self.win_id = "Yelkiran"

        # Other windows
        self.c_win = window.ColorWindow(self.config)
        self.c_win.init()

        # Start the loop
        while True:
            ret, frame = self.capture.read()
            if not self.process(frame):
                break

        # After the loop release the cap object
        self.capture.release()
        # Destroy all the windows
        cv2.destroyAllWindows()

    def process(self, frame) -> bool:
        """Called each frame for process."""
        
        self.c_win.render()

        if self.record:
            self.result.write(frame)  # Save video
        
        if self.preview:
            frame = cv2.resize(frame, (640, 360))
            cv2.imshow(self.win_id, frame)  # Show video

        key = cv2.waitKey(5)
        if key & 0xFF == ord('q'):
            return False

        return True
