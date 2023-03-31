"""Image processing."""
import colorsys
import datetime
import tkinter
import os

import PIL.Image
import PIL.ImageTk
import numpy as np
import cv2

import utilities
import savelog
import binder
import config as conf


class Processor:
    """
    Processor going to call bindings according to processed video.
    """

    bindings: binder.Bindings
    config: conf.ConfigUtil

    preview: bool
    record: bool

    result: cv2.VideoWriter
    capture: cv2.VideoCapture

    def __init__(self):

        # Configuration
        config = conf.ConfigUtil()

        # Unique folder
        self.record_dir = os.path.join(
            config.get_string('general.record-dir'),
            f"recording {datetime.datetime.now().strftime('%d.%m.%Y %H-%M-%S')}"
        )
        if not os.path.exists(self.record_dir):
            os.makedirs(self.record_dir)

        # Logging
        if config.get_bool("general.logging"):
            savelog.initialize(self.record_dir)

        # Bindings
        mode = config.get_string("general.video-source").lower()
        if mode == "simulator":
            # Simulator Mode.
            print("Simulator enabled, trying to connect to the server.")
            self.bindings = binder.Server(config.get_string("simulator.host"), config.get_int("simulator.port"))
        elif mode == "file":
            # File Mode
            self.bindings = binder.File()
        else:
            # Raspberry Pi Mode
            self.bindings = binder.Raspberry()

        self.config = config
        self.preview = self.config.get_bool("general.preview")
        self.record = self.config.get_bool("general.record")

        # Main loop
        self.start_loop()

    def get_capture_size(self) -> tuple[int, int]:
        """Returns the size of the capture."""
        frame_width = int(self.capture.get(3))
        frame_height = int(self.capture.get(4))
        return frame_width, frame_height

    def start_loop(self) -> None:
        """Main loop for image processing."""

        # Get webcam capture
        if self.config.get_string("general.video-source") == "file":
            self.capture = cv2.VideoCapture(self.config.get_string("file.video-path"))
        else:
            self.capture = cv2.VideoCapture(self.config.get_int("general.camera-index"))

        # Fix size for simulator.
        if self.config.get_string("general.video-source") == "simulator":
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        self.capture.set(cv2.CAP_PROP_FPS, 30)

        # Create recording if enabled.
        video_path = os.path.join(self.record_dir, "video_1.avi")
        if self.record:
            size = self.get_capture_size()
            self.result = cv2.VideoWriter(os.path.abspath(video_path), cv2.VideoWriter_fourcc(*'XVID'), float(30), size)

        # WindoW
        if self.preview:
            self.app = tkinter.Tk()
            self.app.title("Yelkiran UAV - Image Processing - Preview")
            self.app.bind("<Escape>", lambda e: self.app.quit())

            cap_canvas = tkinter.Label(self.app)
            cap_canvas.pack()

            hsv_panel = tkinter.Frame(self.app)
            hsv_panel.pack(padx=20, pady=20)
            col_box_panel = tkinter.Frame(self.app)
            col_box_panel.pack(side=tkinter.TOP, padx=20, pady=20)
            buttons_panel = tkinter.Frame(self.app)
            buttons_panel.pack(padx=20, pady=20)

            # Lower HSV Panel
            lower_hsv_panel = tkinter.Frame(hsv_panel)
            lower_hsv_panel.pack(side=tkinter.LEFT)
            tkinter.Label(lower_hsv_panel, text="Lower HSV").pack()

            lower_h_panel = tkinter.Frame(lower_hsv_panel)
            lower_h_panel.pack(side=tkinter.LEFT)
            tkinter.Label(lower_h_panel, text="Hue").pack()
            lower_h = tkinter.Scale(lower_h_panel, from_=0, to=180)
            lower_h.set(self.config.get_int("opencv.lower_h"))
            lower_h.pack()

            lower_s_panel = tkinter.Frame(lower_hsv_panel)
            lower_s_panel.pack(side=tkinter.LEFT)
            tkinter.Label(lower_s_panel, text="Saturation").pack()
            lower_s = tkinter.Scale(lower_s_panel, from_=0, to=255)
            lower_s.set(self.config.get_int("opencv.lower_s"))
            lower_s.pack()

            lower_v_panel = tkinter.Frame(lower_hsv_panel)
            lower_v_panel.pack(side=tkinter.LEFT)
            tkinter.Label(lower_v_panel, text="Value").pack()
            lower_v = tkinter.Scale(lower_v_panel, from_=0, to=255)
            lower_v.set(self.config.get_int("opencv.lower_v"))
            lower_v.pack(side=tkinter.LEFT)

            # Lower HSV Example
            lower_hsv_example = tkinter.Canvas(hsv_panel, width=200, height=100)
            lower_hsv_example.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=True, padx=(10, 0))
            lower_hsv_example_fill = lower_hsv_example.create_rectangle(
                0, 0,
                400, 400,
                fill='#000'
            )

            # Upper HSV Example
            upper_hsv_example = tkinter.Canvas(hsv_panel, width=200, height=100)
            upper_hsv_example.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=True, padx=(0, 10))
            upper_hsv_example_fill = upper_hsv_example.create_rectangle(
                0, 0,
                400, 400,
                fill='#000'
            )

            # Upper HSV Panel
            upper_hsv_panel = tkinter.Frame(hsv_panel)
            upper_hsv_panel.pack(side=tkinter.LEFT)
            tkinter.Label(upper_hsv_panel, text="Upper HSV").pack()

            upper_h_panel = tkinter.Frame(upper_hsv_panel)
            upper_h_panel.pack(side=tkinter.LEFT)
            tkinter.Label(upper_h_panel, text="Hue").pack()
            upper_h = tkinter.Scale(upper_h_panel, from_=0, to=180)
            upper_h.set(self.config.get_int("opencv.upper_h"))
            upper_h.pack()

            upper_s_panel = tkinter.Frame(upper_hsv_panel)
            upper_s_panel.pack(side=tkinter.LEFT)
            tkinter.Label(upper_s_panel, text="Saturation").pack()
            upper_s = tkinter.Scale(upper_s_panel, from_=0, to=255)
            upper_s.set(self.config.get_int("opencv.upper_s"))
            upper_s.pack()

            upper_v_panel = tkinter.Frame(upper_hsv_panel)
            upper_v_panel.pack(side=tkinter.LEFT)
            tkinter.Label(upper_v_panel, text="Value").pack()
            upper_v = tkinter.Scale(upper_v_panel, from_=0, to=255)
            upper_v.set(self.config.get_int("opencv.upper_v"))
            upper_v.pack(side=tkinter.LEFT)

            # Utilities
            def get_upper_hsv():
                """Upper hsv slider variables."""
                return upper_h.get(), upper_s.get(), upper_v.get()

            def get_lower_hsv():
                """Lower hsv slider variables."""
                return lower_h.get(), lower_s.get(), lower_v.get()

            # Listen for events
            def update_upper_canvas(*args):
                h, s, v = get_upper_hsv()
                rgb = np.array(colorsys.hsv_to_rgb(h / 180, s / 255, v / 255)) * 255
                rgb = np.uint32(rgb)
                self.upper_hsv = np.array([h, s, v], np.uint8)

                upper_hsv_example.itemconfigure(
                    upper_hsv_example_fill,
                    {
                        "fill": '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
                    }
                )

            upper_h.configure(command=update_upper_canvas)
            upper_s.configure(command=update_upper_canvas)
            upper_v.configure(command=update_upper_canvas)

            def update_lower_canvas(*args):
                h, s, v = get_lower_hsv()
                rgb = np.array(colorsys.hsv_to_rgb(h / 180, s / 255, v / 255)) * 255
                rgb = np.uint32(rgb)
                self.lower_hsv = np.array([h, s, v], np.uint8)

                lower_hsv_example.itemconfigure(
                    lower_hsv_example_fill,
                    {
                        "fill": '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
                    }
                )

            lower_h.configure(command=update_lower_canvas)
            lower_s.configure(command=update_lower_canvas)
            lower_v.configure(command=update_lower_canvas)

            # Initial update
            update_upper_canvas()
            update_lower_canvas()

            # Collision Box Configuration
            col_box_size_panel = tkinter.Frame(col_box_panel)
            col_box_size_panel.pack(side=tkinter.LEFT)
            col_box_offset_panel = tkinter.Frame(col_box_panel)
            col_box_offset_panel.pack(side=tkinter.RIGHT)

            # Width input
            col_box_width_panel = tkinter.Frame(col_box_size_panel)
            col_box_width_panel.pack()
            tkinter.Label(col_box_width_panel, text="Width: ").pack(side=tkinter.LEFT)
            col_box_width_sb = tkinter.Spinbox(col_box_width_panel, from_=-300, to=300)
            col_box_width_sb.pack()

            # Height input
            col_box_height_panel = tkinter.Frame(col_box_size_panel)
            col_box_height_panel.pack()
            tkinter.Label(col_box_height_panel, text="Height: ").pack(side=tkinter.LEFT)
            col_box_height_sb = tkinter.Spinbox(col_box_height_panel, from_=-300, to=300)
            col_box_height_sb.pack()

            # Horizontal offset
            col_box_horizontal_offset_panel = tkinter.Frame(col_box_offset_panel)
            col_box_horizontal_offset_panel.pack()
            tkinter.Label(col_box_horizontal_offset_panel, text="Horizontal Offset: ").pack(side=tkinter.LEFT)
            col_box_horizontal_offset_sb = tkinter.Spinbox(col_box_horizontal_offset_panel, from_=-300, to=300)
            col_box_horizontal_offset_sb.pack()

            # Vertical offset
            col_box_vertical_offset_panel = tkinter.Frame(col_box_offset_panel)
            col_box_vertical_offset_panel.pack()
            tkinter.Label(col_box_vertical_offset_panel, text="Vertical Offset: ").pack(side=tkinter.LEFT)
            col_box_vertical_offset_sb = tkinter.Spinbox(col_box_vertical_offset_panel, from_=-300, to=300)
            col_box_vertical_offset_sb.pack()
            
            def get_collision_box_data() -> tuple[int, int, int, int]:
                """Returns collision box data"""
                return \
                    int(col_box_width_sb.get()) if col_box_width_sb.get().lstrip('-').isdigit() else 0, \
                    int(col_box_height_sb.get()) if col_box_height_sb.get().lstrip('-').isdigit() else 0, \
                    int(col_box_horizontal_offset_sb.get()) if col_box_horizontal_offset_sb.get().lstrip('-').isdigit() else 0, \
                    int(col_box_vertical_offset_sb.get()) if col_box_vertical_offset_sb.get().lstrip('-').isdigit() else 0
                
            def update_collision_box_data():
                """global collision data."""
                self.box_collision_width, \
                self.box_collision_height, \
                self.box_collision_horizontal, \
                self.box_collision_vertical \
                = get_collision_box_data()
            
            def fill_collision_box_data() -> None:
                """Fills collision box data according to config."""
                col_box_width_sb.delete(0, "end")
                col_box_height_sb.delete(0, "end")
                col_box_horizontal_offset_sb.delete(0, "end")
                col_box_vertical_offset_sb.delete(0, "end")
                col_box_width_sb.insert(0, self.config.get_string("opencv.collision-box-width"))
                col_box_height_sb.insert(0, self.config.get_string("opencv.collision-box-height"))
                col_box_horizontal_offset_sb.insert(0, self.config.get_string("opencv.collision-box-horizontal-offset"))
                col_box_vertical_offset_sb.insert(0, self.config.get_string("opencv.collision-box-vertical-offset"))

            fill_collision_box_data()
            update_collision_box_data()
            col_box_width_sb.configure(command=update_collision_box_data)
            col_box_height_sb.configure(command=update_collision_box_data)
            col_box_horizontal_offset_sb.configure(command=update_collision_box_data)
            col_box_vertical_offset_sb.configure(command=update_collision_box_data)

            # Buttons
            def save():
                """Save changes."""
                h, s, v = get_upper_hsv()
                self.config.set_field("opencv.upper_h", str(h))
                self.config.set_field("opencv.upper_s", str(s))
                self.config.set_field("opencv.upper_v", str(v))

                h, s, v = get_lower_hsv()
                self.config.set_field("opencv.lower_h", str(h))
                self.config.set_field("opencv.lower_s", str(s))
                self.config.set_field("opencv.lower_v", str(v))

                width, height, horizontal, vertical = get_collision_box_data()
                self.config.set_field("opencv.collision-box-width", str(width))
                self.config.set_field("opencv.collision-box-height", str(height))
                self.config.set_field("opencv.collision-box-horizontal-offset", str(horizontal))
                self.config.set_field("opencv.collision-box-vertical-offset", str(vertical))

                self.config.save()

            def discard():
                """Discard changes"""
                upper_h.set(self.config.get_int("opencv.upper_h"))
                upper_v.set(self.config.get_int("opencv.upper_v"))
                upper_s.set(self.config.get_int("opencv.upper_s"))
                lower_h.set(self.config.get_int("opencv.lower_h"))
                lower_s.set(self.config.get_int("opencv.lower_s"))
                lower_v.set(self.config.get_int("opencv.lower_v"))
                fill_collision_box_data()

            def quit_command():
                self.app.quit()

            tkinter.Button(buttons_panel, text="Save Changes", command=save).pack(side=tkinter.LEFT, padx=5)
            tkinter.Button(buttons_panel, text="Discard", command=discard).pack(side=tkinter.LEFT, padx=5)
            tkinter.Button(buttons_panel, text="Quit", command=quit_command).pack(side=tkinter.LEFT, padx=5)
        else:
            self.upper_hsv = np.array([self.config.get_int("opencv.upper_h"), self.config.get_int("opencv.upper_s"), self.config.get_int("opencv.upper_v")], np.uint8)
            self.lower_hsv = np.array(  [self.config.get_int("opencv.lower_h"), self.config.get_int("opencv.lower_s"), self.config.get_int("opencv.lower_v")], np.uint8)
            self.box_collision_width, \
                self.box_collision_height, \
                self.box_collision_horizontal, \
                self.box_collision_vertical \
                = \
                self.config.get_int("opencv.collision-box-width"), \
                self.config.get_int("opencv.collision-box-height"), \
                self.config.get_int("opencv.collision-box-horizontal-offset"), \
                self.config.get_int("opencv.collision-box-vertical-offset")

        def process():

            ret, frame = self.capture.read()

            if not ret:
                self.capture.set(1, 0)
                return

            frame_h, frame_w = frame.shape[:2]

            box_start_x, \
                box_start_y, \
                box_end_x, \
                box_end_y = \
                int(frame_w / 2 - self.box_collision_width / 2 + self.box_collision_horizontal), \
                    int(frame_h / 2 - self.box_collision_height / 2 + self.box_collision_vertical), \
                    int(frame_w / 2 + self.box_collision_width / 2 + self.box_collision_horizontal), \
                    int(frame_h / 2 + self.box_collision_height / 2 + self.box_collision_vertical)

            # Create the mask
            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(frame_hsv, self.lower_hsv, self.upper_hsv)

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
                    self.collided = True
                    self.bindings.open_package_door()
            else:
                self.collided = False
                
            # Record Video
            if self.record:
                self.result.write(frame)

            if self.preview:

                # Special visualizations for preview
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

                cap_canvas.imgtk = imgtk
                cap_canvas.configure(image=imgtk)

        # Start the loop
        if self.preview:

            def mainloop():
                """Called each frame for process."""
                process()
                cap_canvas.after(5, mainloop)

            mainloop()
            self.app.mainloop()

        else:

            while True:
                process()
                cv2.waitKey(5)

        self.capture.release()
