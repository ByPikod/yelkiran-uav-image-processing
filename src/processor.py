"""Image processing."""
import colorsys
import datetime
import tkinter
import os

import PIL.Image
import PIL.ImageTk
import numpy as np
import cv2

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
        self.record_dir = f"recording {datetime.datetime.now().strftime('%d.%m.%Y %H-%M-%S')}"

        # Logging
        if config.get_bool("general.logging"):
            savelog.initialize(self.record_dir)

        # Bindings
        mode = config.get_string("general.video-source").lower()
        if mode == "simulator":
            # Simulator Mode.
            print("Simulator enabled, trying to connect to the server.")
            self.binding = binder.Server(config.get_string("simulator.host"), config.get_int("simulator.port"))
        elif mode == "file":
            # File Mode
            self.binding = binder.File()
        else:
            # Raspberry Pi Mode
            self.binding = binder.Raspberry()

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
        if self.config.get_string("general.video-source"):
            self.capture = cv2.VideoCapture(self.config.get_string("file.video-path"))
        else:
            self.capture = cv2.VideoCapture(self.config.get_int("general.camera-index"))

        # Fix size for simulator.
        if self.config.get_bool("simulator.enabled"):
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Create recording if enabled.
        video_path = os.path.join(self.record_dir, "video.avi")
        if self.record:
            size = self.get_capture_size()
            self.result = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'XVID'), 30, size)
    
        # Window
        self.app = tkinter.Tk()
        self.app.title("Yelkiran UAV - Image Processing - Preview")
        self.app.bind("<Escape>", lambda e: self.app.quit())
        
        cap_canvas = tkinter.Label(self.app)
        cap_canvas.pack()

        hsv_panel = tkinter.Frame(self.app)
        hsv_panel.pack(padx=20, pady=20)
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

            self.config.save()

        def discard():
            """Discard changes"""
            upper_h.set(self.config.get_int("opencv.upper_h"))
            upper_v.set(self.config.get_int("opencv.upper_v"))
            upper_s.set(self.config.get_int("opencv.upper_s"))
            lower_h.set(self.config.get_int("opencv.lower_h"))
            lower_s.set(self.config.get_int("opencv.lower_s"))
            lower_v.set(self.config.get_int("opencv.lower_v"))

        def quit_command():
            self.app.quit()

        tkinter.Button(buttons_panel, text="Save Changes", command=save).pack(side=tkinter.LEFT, padx=5)
        tkinter.Button(buttons_panel, text="Discard", command=discard).pack(side=tkinter.LEFT, padx=5)
        tkinter.Button(buttons_panel, text="Quit", command=quit_command).pack(side=tkinter.LEFT, padx=5)

        # Start the loop
        
        def process():
            """Called each frame for process."""

            def task():
                ret, frame = self.capture.read()
                
                if not ret:
                    self.capture.set(1, 0)
                    return

                if self.record:
                    self.result.write(frame)  # Save video
                
                frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(frame_hsv, self.lower_hsv, self.upper_hsv)
                output = cv2.bitwise_and(frame_hsv, frame_hsv, mask=mask)
                output = cv2.cvtColor(output, cv2.COLOR_HSV2RGB)

                if self.preview:
                    
                    # Resize
                    frame = cv2.resize(frame, (640, 360))
                    output = cv2.resize(output, (640, 360))

                    # Color convert
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Final Output
                    frame = cv2.hconcat([frame, output])
                    
                    img = PIL.Image.fromarray(frame)
                    imgtk = PIL.ImageTk.PhotoImage(image=img)

                    cap_canvas.imgtk = imgtk
                    cap_canvas.configure(image=imgtk)

            # Loop
            task()
            cap_canvas.after(5, process)
            

        process()
        self.app.mainloop()
        self.capture.release()
