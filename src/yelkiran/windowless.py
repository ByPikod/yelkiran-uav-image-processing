from . import properties

import numpy as np


class Windowedless(properties.Properties):
    
    def __init__(self) -> None:
    
        self.upper_hsv = np.array(
            [
                self.config.get_int("opencv.upper_h"), 
                self.config.get_int("opencv.upper_s"), 
                self.config.get_int("opencv.upper_v")
            ], 
            np.uint8
        )
        
        self.lower_hsv = np.array(
            [
                self.config.get_int("opencv.lower_h"), 
                self.config.get_int("opencv.lower_s"),
                self.config.get_int("opencv.lower_v")
            ],
            np.uint8
        )
        
        self.box_collision_width, \
            self.box_collision_height, \
            self.box_collision_horizontal, \
            self.box_collision_vertical \
            = \
            self.config.get_int("opencv.collision-box-width"), \
            self.config.get_int("opencv.collision-box-height"), \
            self.config.get_int("opencv.collision-box-horizontal-offset"), \
            self.config.get_int("opencv.collision-box-vertical-offset")