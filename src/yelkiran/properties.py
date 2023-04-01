import numpy as np


class Properties:
    """Wraps properties as fields for processor."""
    
    upper_hsv: np.array
    lower_hsv: np.array
    
    box_collision_width: int
    box_collision_height: int
    box_collision_horizontal_offset: int
    box_collision_vertical_offset: int