from typing import Tuple

import threading
import time

import numpy as np
import cv2

class PeriodicTimer:
    """
    Periodic timer can be cancelled without waiting through the cooldown
    thanks to its algorithm which is sleeping in specified periods. 
    """
    __cancel: bool = False
    
    def __init__(
            self, 
            delay: float, 
            period: float, 
            callback: callable
        ) -> None:
        
        self.delay = delay
        self.period = period
        self.callback = callback
    
    def loop(self) -> None:
        """
        Call the callback function when wait ends.
        """
        
        while self.delay > 0:
            self.delay = self.delay - self.period
            time.sleep(self.period)
            if self.__cancel:
                return
            
        self.callback()
    
    def start(self) -> None:
        """
        Start waiting.
        """
        
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()
    
    def cancel(self) -> None:
        """
        Cancel the callback.
        """
        self.__cancel = True


def draw_square(
        frame: np.ndarray,
        start: Tuple[int, int],
        end: Tuple[int, int],
        color: Tuple[int, int, int],
        thickness: int
) -> None:
    """
    Draw better looking square.
    :param frame: OpenCV frame
    :param start: Start corner tuple.
    :param end: Opposite corner tuple.
    :param color: Color tuple
    :param thickness: Thickness of the lines
    """

    width = start[0] - end[0]
    height = start[1] - end[1]

    # Top Left
    cv2.line(
        frame,
        (start[0], start[1]),
        (start[0] - int(width * 0.2), start[1]),
        color,
        thickness
    )
    cv2.line(
        frame,
        (start[0], start[1]),
        (start[0], start[1] - int(height * 0.2)),
        color,
        thickness
    )

    # Top Right
    cv2.line(
        frame,
        (end[0], start[1]),
        (end[0] + int(width * 0.2), start[1]),
        color,
        thickness
    )
    cv2.line(
        frame,
        (end[0], start[1]),
        (end[0], start[1] - int(width * 0.2)),
        color,
        thickness
    )

    # Bottom Left
    cv2.line(
        frame,
        (start[0], end[1]),
        (start[0] - int(width * 0.2), end[1]),
        color,
        thickness
    )
    cv2.line(
        frame,
        (start[0], end[1]),
        (start[0], end[1] + int(width * 0.2)),
        color,
        thickness
    )

    # Bottom Right
    cv2.line(
        frame,
        (end[0], end[1]),
        (end[0] + int(width * 0.2), end[1]),
        color,
        thickness
    )
    cv2.line(
        frame,
        (end[0], end[1]),
        (end[0], end[1] + int(width * 0.2)),
        color,
        thickness
    )
