"""Image processing."""
import datetime
import os

import PIL.Image
import PIL.ImageTk
import cv2

from . import properties
from . import windowed
from . import windowless
from . import utilities
from . import savelog
from . import binder
from . import config as conf


class Processor:
    """
    Processor going to call bindings according to processed video.
    """

    bindings: binder.Bindings
    properties: properties.Properties
    config: conf.ConfigUtil

    preview: bool
    record: bool
    
    collided: bool = False

    result: cv2.VideoWriter
    capture: cv2.VideoCapture


    def __init__(self):

        # Configuration
        config = conf.ConfigUtil()
        self.config = config
        self.preview = self.config.get_bool("general.preview")
        self.record = self.config.get_bool("general.record")
        self.logging = config.get_bool("general.logging")
        
        # Unique folder
        self.record_dir = os.path.abspath(os.path.join(
            config.get_string('general.record-dir'),
            f"recording {datetime.datetime.now().strftime('%d.%m.%Y %H-%M-%S')}"
        ))
        if (
            not os.path.exists(self.record_dir) and
            (self.logging or self.record)
        ): os.makedirs(self.record_dir)
        
        # Logging
        if self.logging:
            savelog.initialize(self.record_dir)

        print(f"""Information:
Output directory: {self.record_dir}
Preview:\t{'Enabled' if self.preview else 'Disabled'}
Recording:\t{'Enabled' if self.record else 'Disabled'}
Logging:\t{'Enabled' if self.logging else 'Disabled'}"""
        )
        
        # Bindings
        mode = config.get_string("general.video-source").lower()
        if mode == "simulator":
            # Simulator Mode.
            print("Binder: Simulator")
            print("Connecting to the server...")
            self.bindings = binder.Server(config.get_string("simulator.host"), config.get_int("simulator.port"))
        elif mode == "file":
            # File Mode
            print("Binder: Free")
            self.bindings = binder.Bindings()
        else:
            # Raspberry Pi Mode
            print("Binder: Raspberry")
            self.bindings = binder.Raspberry()

        # Get webcam capture
        if self.config.get_string("general.video-source") == "file":
            src_video_path = self.config.get_string("file.video-path")
            print(f"Capture initializing with file #{src_video_path}")
            self.capture = cv2.VideoCapture(src_video_path)
        else:
            cam = self.config.get_int("general.camera-index")
            print(f"Capture initializing with video input #{cam}")
            self.capture = cv2.VideoCapture(cam)
            if self.capture.isOpened(): print("Capture opened!")

        # Fix size for simulator.
        if self.config.get_string("general.video-source") == "simulator":
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        else:
            self.capture.set(cv2.CAP_PROP_FPS, 30)

        # Main loop
        self.start_loop()


    def get_capture_size(self) -> tuple[int, int]:
        """Returns the size of the capture."""
        frame_width = int(self.capture.get(3))
        frame_height = int(self.capture.get(4))
        return frame_width, frame_height
    

    def start_loop(self) -> None:
        """Main loop for image processing."""

        # Create recording if enabled.
        video_path = os.path.join(self.record_dir, "video.avi")
        num = 0
        while os.path.isfile(video_path):
            num = num + 1
            video_path = os.path.join(self.record_dir, f"video_{num}.avi")
        if self.record and self.bindings.power():
            print(f"Recording video: {video_path}")
            size = self.get_capture_size()
            self.result = cv2.VideoWriter(os.path.abspath(video_path), cv2.VideoWriter_fourcc(*'XVID'), float(30), size)
            print("Record started.")
        
        # Windowed
        if self.preview:
            
            self.properties = windowed.Windowed(self.config)
            print("Properties set to window.")
            
            def mainloop():
                """Called each frame for process."""
                if self.capture.isOpened() and self.bindings.power():
                    self.process()
                    self.properties.capture_canvas.after(5, mainloop)
                else:
                    
                    print("Record over.")
                    # self.capture.release()
                    
                    while not self.bindings.power():
                        cv2.waitKey(100)
                        
                    self.start_loop()
                        
                
            mainloop()
            print("Process loop started.")
            self.properties.app.mainloop()
            
        # Windowless
        else:
            
            self.properties = windowless.Windowedless(self.config)
            print("Properties set to config.")

            while self.capture.isOpened() and self.bindings.power():
                self.process()
                cv2.waitKey(5)
            
            print("Record over.")
            # self.capture.release()
            
            while not self.bindings.power():
                cv2.waitKey(100)
            
            self.start_loop()


    def process(self):
        """Grab the frame and process"""
        
        ret, frame = self.capture.read()

        if not ret:
            self.capture.set(1, 0)
            return

        frame_h, frame_w = frame.shape[:2]

        box_start_x, \
            box_start_y, \
            box_end_x, \
            box_end_y = \
            int(
                frame_w / 2 
                - self.properties.box_collision_width / 2 
                + self.properties.box_collision_horizontal
            ), \
            int(
                frame_h / 2 
                - self.properties.box_collision_height / 2 
                + self.properties.box_collision_vertical
            ), \
            int(frame_w / 2 
            + self.properties.box_collision_width / 2 
            + self.properties.box_collision_horizontal
            ), \
            int(frame_h / 2 
            + self.properties.box_collision_height / 2 
            + self.properties.box_collision_vertical
            )

        # Create the mask
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(
            frame_hsv, 
            self.properties.lower_hsv, 
            self.properties.upper_hsv
        )

        # Find contours.
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Calculate center of the color
        cx, cy = 0, 0
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            cmoments = cv2.moments(c)
            try:
                cx, cy = \
                int(cmoments['m10'] / cmoments['m00']), \
                int(cmoments['m01'] / cmoments['m00'])
            except ZeroDivisionError:
                return

        # If detected object is colliding with the box.
        collision_state = (
            box_start_x < cx < box_end_x and
            box_start_y < cy < box_end_y
        )

        # Drop the ball
        if collision_state:
            if not self.collided:
                print("Collision detected.")
                self.collided = True
                self.bindings.open_package_door()
        elif self.collided:
            self.collided = False
            print("Collision over.")
                
        # Record Video
        if self.record:
            self.result.write(frame)
        
        # Special visualizations for preview
        if self.preview:
            output = cv2.bitwise_and(frame_hsv, frame_hsv, mask=mask)
            output = cv2.cvtColor(output, cv2.COLOR_HSV2RGB)

            if len(contours) > 0:
                # cv2.drawContours(output, contours, 0, (255, 255, 255), 2)
                cv2.circle(frame, (cx, cy), 10, (255, 255, 255), -1)
                cv2.line(frame, (cx, 0), (cx, cy - 40), (255, 255, 255), 3)
                cv2.line(frame, (cx, frame_h), (cx, cy + 40), (255, 255, 255), 3)
                cv2.line(frame, (0, cy), (cx - 40, cy), (255, 255, 255), 3)
                cv2.line(frame, (frame_w, cy), (cx + 40, cy), (255, 255, 255), 3)

            collision_color = (0, 255, 0) if collision_state else (255, 255, 255)
            utilities.draw_square(
                frame,
                (box_start_x, box_start_y),
                (box_end_x, box_end_y),
                collision_color,
                3
            )

            # Resize
            frame = cv2.resize(frame, (640, 360))
            output = cv2.resize(output, (640, 360))

            # Color convert
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Final Output
            final_output = cv2.hconcat([frame, output])

            img = PIL.Image.fromarray(final_output)
            imgtk = PIL.ImageTk.PhotoImage(image=img)
                
            self.properties.capture_canvas.imgtk = imgtk
            self.properties.capture_canvas.configure(image=imgtk)
