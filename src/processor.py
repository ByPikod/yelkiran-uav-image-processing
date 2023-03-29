from configparser import ConfigParser

import cv2
import numpy as np

from bindings import Bindings


class Processor:
    """
    Processor going to call bindings according to processed video.
    """

    bindings: Bindings
    simulator: bool

    def __init__(self, bindings: Bindings, config: ConfigParser):
        
        self.bindings = bindings
        self.config = config

        try:
            self.process()
        except cv2.error as err:
            print(f"An error has occurred while processing video camera: \n{err}")

    def process(self):
        """Main loop for image processing."""

        vid = cv2.VideoCapture(int(self.config["GENERAL"]["camera-index"]))

        if self.config["SIMULATOR"]["enabled"]:
            vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:
            ret, frame = vid.read()
            cv2.imshow('Recording', frame)

            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

        # After the loop release the cap object
        vid.release()

        # Destroy all the windows
        cv2.destroyAllWindows()
