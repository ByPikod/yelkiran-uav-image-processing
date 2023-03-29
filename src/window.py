import config

import cv2
import numpy as np


class Window:

    __enabled: bool = False

    def __init__(self) -> None:
        pass

    def init(self) -> None:
        """Initializes the window, consider not using manually."""
        cv2.namedWindow(self.get_win_title(), self.get_win_flags())
        self.create()

    def render(self) -> None:
        """Renders window by calling imshow each frame."""
        cv2.imshow(self.get_win_title(), self.get_win_image())
    
    def get_win_flags(self) -> int:
        return cv2.WINDOW_KEEPRATIO

    def get_win_title(self) -> str:
        pass
    
    def get_win_image(self) -> any:
        pass

    def create(self) -> None:
        pass

class ColorWindow(Window):

    def __init__(self, config: config.ConfigUtil) -> None:
        self.config = config

    def get_win_title(self) -> str:
        return "HSV Adjustment"

    def get_win_image(self) -> any:
        return self.image
    
    def render(self) -> None:
        super().render()

    def update_image(self):

        h, s, v = \
            cv2.getTrackbarPos("Upper H", self.get_win_title()), \
            cv2.getTrackbarPos("Upper S", self.get_win_title()), \
            cv2.getTrackbarPos("Upper V", self.get_win_title())
            
        self.upper_hsv = [h, s, v]
        
        h, s, v = \
            cv2.getTrackbarPos("Lower H", self.get_win_title()), \
            cv2.getTrackbarPos("Lower S", self.get_win_title()), \
            cv2.getTrackbarPos("Lower V", self.get_win_title())
        
        self.lower_hsv = [h, s, v]

        self.upper_img[:] = self.upper_hsv 
        self.lower_img[:] = self.lower_hsv
            
        self.image = cv2.hconcat([self.upper_img, self.lower_img])

    def create(self) -> None:

        def trackbar_update(*args):
            self.update_image()
            
        def save_color_range(*args):
            pass

        cv2.createTrackbar("Upper H", self.get_win_title(), 0, 180, trackbar_update)
        cv2.createTrackbar("Upper S", self.get_win_title(), 0, 255, trackbar_update)
        cv2.createTrackbar("Upper V", self.get_win_title(), 0, 255, trackbar_update)
        cv2.createTrackbar("Lower H", self.get_win_title(), 0, 180, trackbar_update)
        cv2.createTrackbar("Lower S", self.get_win_title(), 0, 255, trackbar_update)
        cv2.createTrackbar("Lower V", self.get_win_title(), 0, 255, trackbar_update)
        
        cv2.createButton("Save", save_color_range, None, cv2.QT_PUSH_BUTTON, 1)

        
        self.upper_img = np.zeros((100, 100, 3), np.uint8)
        self.lower_img = np.zeros((100, 100, 3), np.uint8)
        self.update_image()