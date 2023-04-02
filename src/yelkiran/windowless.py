from . import properties

import numpy as np


class Windowedless(properties.Properties):
    
    def __init__(self, config) -> None:
    
        self.upper_hsv = np.array(
            [
                config.get_int("opencv.upper_h"), 
                config.get_int("opencv.upper_s"), 
                config.get_int("opencv.upper_v")
            ], 
            np.uint8
        )
        
        self.lower_hsv = np.array(
            [
                config.get_int("opencv.lower_h"), 
                config.get_int("opencv.lower_s"),
                config.get_int("opencv.lower_v")
            ],
            np.uint8
        )
        
        self.box_collision_width, \
            self.box_collision_height, \
            self.box_collision_horizontal, \
            self.box_collision_vertical \
            = \
            config.get_int("opencv.collision-box-width"), \
            config.get_int("opencv.collision-box-height"), \
            config.get_int("opencv.collision-box-horizontal-offset"), \
            config.get_int("opencv.collision-box-vertical-offset")
        
        print(
            f"""Properties:
Upper HSV:\t{str(self.upper_hsv.tolist())}
Lower HSV:\t{str(self.lower_hsv.tolist())}
Col width:\t{self.box_collision_width}
Col height:\t{self.box_collision_height}
Col horizontal:\t{self.box_collision_horizontal}
Col vertical:\t{self.box_collision_vertical}"""
        )