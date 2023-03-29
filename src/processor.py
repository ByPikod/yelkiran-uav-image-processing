import datetime
import os

import logging
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

    def __init__(self):

        # Configuration
        config = conf.get_config()

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

        try:
            self.process()
        except cv2.error as err:
            print(f"An error has occurred while processing video camera: \n{err}")

    def process(self):
        """Main loop for image processing."""

        vid = cv2.VideoCapture(self.config.get_int("general.camera-index"))

        if self.config.get_bool("simulator.enabled"):
            vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Get size
        frame_width = int(vid.get(3))
        frame_height = int(vid.get(4))
        size = (frame_width, frame_height)

        # Create recording
        video_path = os.path.join(self.record_dir, "video.avi")
        result = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'XVID'), 30, size)

        preview = self.config.get_bool("general.preview")
        record = self.config.get_bool("general.record")

        while True:

            ret, frame = vid.read()

            if record:
                result.write(frame)  # Save video

            if preview:
                cv2.imshow('Recording', frame)  # Show video

            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

        # After the loop release the cap object
        vid.release()
        result.release()

        # Destroy all the windows
        cv2.destroyAllWindows()
