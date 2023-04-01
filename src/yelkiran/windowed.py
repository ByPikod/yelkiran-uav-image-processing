from . import properties

import tkinter
import numpy as np
import colorsys


class Windowed(properties.Properties):
    
    def __init__(self, config) -> None:
    
        self.app = tkinter.Tk()
        self.app.title("Yelkiran UAV - Image Processing - Preview")
        self.app.bind("<Escape>", lambda e: self.app.quit())
    
        self.capture_canvas = tkinter.Label(self.app)
        self.capture_canvas.pack()
    
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
        lower_h.set(config.get_int("opencv.lower_h"))
        lower_h.pack()
    
        lower_s_panel = tkinter.Frame(lower_hsv_panel)
        lower_s_panel.pack(side=tkinter.LEFT)
        tkinter.Label(lower_s_panel, text="Saturation").pack()
        lower_s = tkinter.Scale(lower_s_panel, from_=0, to=255)
        lower_s.set(config.get_int("opencv.lower_s"))
        lower_s.pack()
    
        lower_v_panel = tkinter.Frame(lower_hsv_panel)
        lower_v_panel.pack(side=tkinter.LEFT)
        tkinter.Label(lower_v_panel, text="Value").pack()
        lower_v = tkinter.Scale(lower_v_panel, from_=0, to=255)
        lower_v.set(config.get_int("opencv.lower_v"))
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
        upper_h.set(config.get_int("opencv.upper_h"))
        upper_h.pack()
    
        upper_s_panel = tkinter.Frame(upper_hsv_panel)
        upper_s_panel.pack(side=tkinter.LEFT)
        tkinter.Label(upper_s_panel, text="Saturation").pack()
        upper_s = tkinter.Scale(upper_s_panel, from_=0, to=255)
        upper_s.set(config.get_int("opencv.upper_s"))
        upper_s.pack()
    
        upper_v_panel = tkinter.Frame(upper_hsv_panel)
        upper_v_panel.pack(side=tkinter.LEFT)
        tkinter.Label(upper_v_panel, text="Value").pack()
        upper_v = tkinter.Scale(upper_v_panel, from_=0, to=255)
        upper_v.set(config.get_int("opencv.upper_v"))
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
            col_box_width_sb.insert(0, config.get_string("opencv.collision-box-width"))
            col_box_height_sb.insert(0, config.get_string("opencv.collision-box-height"))
            col_box_horizontal_offset_sb.insert(0, config.get_string("opencv.collision-box-horizontal-offset"))
            col_box_vertical_offset_sb.insert(0, config.get_string("opencv.collision-box-vertical-offset"))
    
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
            config.set_field("opencv.upper_h", str(h))
            config.set_field("opencv.upper_s", str(s))
            config.set_field("opencv.upper_v", str(v))
    
            h, s, v = get_lower_hsv()
            config.set_field("opencv.lower_h", str(h))
            config.set_field("opencv.lower_s", str(s))
            config.set_field("opencv.lower_v", str(v))
    
            width, height, horizontal, vertical = get_collision_box_data()
            config.set_field("opencv.collision-box-width", str(width))
            config.set_field("opencv.collision-box-height", str(height))
            config.set_field("opencv.collision-box-horizontal-offset", str(horizontal))
            config.set_field("opencv.collision-box-vertical-offset", str(vertical))
    
            config.save()
    
        def discard():
            """Discard changes"""
            upper_h.set(config.get_int("opencv.upper_h"))
            upper_v.set(config.get_int("opencv.upper_v"))
            upper_s.set(config.get_int("opencv.upper_s"))
            lower_h.set(config.get_int("opencv.lower_h"))
            lower_s.set(config.get_int("opencv.lower_s"))
            lower_v.set(config.get_int("opencv.lower_v"))
            fill_collision_box_data()
    
        def quit_command():
            self.app.quit()
    
        tkinter.Button(buttons_panel, text="Save Changes", command=save).pack(side=tkinter.LEFT, padx=5)
        tkinter.Button(buttons_panel, text="Discard", command=discard).pack(side=tkinter.LEFT, padx=5)
        tkinter.Button(buttons_panel, text="Quit", command=quit_command).pack(side=tkinter.LEFT, padx=5)
        
        print("Window created.")
        