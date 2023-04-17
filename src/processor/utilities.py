import cv2

import numpy as np


def draw_square(
        frame: np.ndarray,
        start: tuple[int, int],
        end: tuple[int, int],
        color: tuple[int, int, int],
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
