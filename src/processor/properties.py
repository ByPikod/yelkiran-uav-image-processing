import tkinter as tk

import numpy as np


class Properties:
    """Wraps properties as fields for processor."""
    
    upper_hsv: np.array
    lower_hsv: np.array
    
    box_collision_width: int
    box_collision_height: int
    box_collision_horizontal: int
    box_collision_vertical: int

    # Optional properties
    app: tk.Tk
    capture_canvas: tk.Label
