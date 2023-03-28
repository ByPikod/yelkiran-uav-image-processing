import cv2
import numpy as np

from bindings import Bindings


"""
Processor going to call bindings according to processed video.
"""


class Processor:

    bindings: Bindings
    simulator: bool

    def __init__(self, bindings: Bindings, simulator: bool):
        self.bindings = bindings
        self.simulator = simulator
        try:
            self.process()
        except cv2.error as err:
            print(f"An error has occurred while processing video camera: \n{err}")

    def process(self):

        vid = cv2.VideoCapture(1 + cv2.CAP_DSHOW)

        if self.simulator:
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
