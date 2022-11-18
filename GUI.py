from tkinter import ttk, font, IntVar
from PIL import Image, ImageTk
from PLUGINS import *

import tkinter as tk
import sv_ttk
import json
import cv2

# Open json and store data in python dict
with open('./config.json', 'r') as f:
    data = json.load(f)


class Tab1(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        class Menu_Bar(ttk.Frame):
            def __init__(self, parent):
                super().__init__(parent, padding=data['paddingSize']['frame'])

                # Power Switch
                self.toggle_switch_1 = IntVar()
                self.switch_1 = ttk.Checkbutton(self, style="Switch.TCheckbutton", variable=self.toggle_switch_1, text="Power", command=lambda: switchPower(root, self.toggle_switch_1))

                # Control Switch
                self.toggle_switch_2 = IntVar()
                self.switch_2 = ttk.Checkbutton(self, style="Switch.TCheckbutton", variable=self.toggle_switch_2, text="Control Mode", command=lambda: switchControlMode(self.toggle_switch_2))

                # Quit GUI
                self.button_1 = ttk.Button(self, style="Toggle.TButton", text="❌", command=lambda: systemShutdown(root))

                # Layout
                self.switch_1.pack(padx=(0, 4), side='left')
                self.switch_2.pack(padx=(4, 4), side='left')
                self.button_1.pack(padx=(4, 0), side='right')
                self.switch_1.shouldToggle = False
                self.button_1.shouldToggle = False
                self.bindings()

            def bindings(self):
                root.bind("<KeyPress-Escape>", lambda event: keyPress(self.button_1, True))
                root.bind("<KeyRelease-Escape>", lambda event: keyPress(self.button_1, False))

        class Box_1(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text="ODrive", padding=data['paddingSize']['labelFrame'])

                class add_widgets_top(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        for index in range(2):
                            self.columnconfigure(index, weight=1, uniform='1')
                        for index in (0, 2, 4):
                            self.rowconfigure(index, weight=1, minsize=data['rowSize']['label'])
                        for index in (1, 3, 5):
                            self.rowconfigure(index, weight=1, minsize=data['rowSize']['progressBar'])

                        # MOSFET M1
                        self.label_1 = ttk.Label(self, text='MOSFET M1')
                        self.output_1 = ttk.Label(self, text='°C')
                        self.progress_1 = ttk.Progressbar(self, value=0, mode="determinate")

                        # MOSFET M2
                        self.label_2 = ttk.Label(self, text='MOSFET M2')
                        self.output_2 = ttk.Label(self, text='°C')
                        self.progress_2 = ttk.Progressbar(self, value=0, mode="determinate")

                        # MOSFET BRAKES
                        self.label_3 = ttk.Label(self, text='MOSFET BRAKES')
                        self.output_3 = ttk.Label(self, text='°C')
                        self.progress_3 = ttk.Progressbar(self, value=0, mode="determinate")

                        # Layout
                        self.label_1.grid(row=0, column=0, pady=(4, 4), sticky="W")
                        self.output_1.grid(row=0, column=1, pady=(4, 4), sticky="E")
                        self.progress_1.grid(row=1, columnspan=2, sticky="NEW")

                        self.label_2.grid(row=2, column=0, pady=(4, 4), sticky="W")
                        self.output_2.grid(row=2, column=1, pady=(4, 4), sticky="E")
                        self.progress_2.grid(row=3, columnspan=2, sticky="NEW")

                        self.label_3.grid(row=4, column=0, pady=(4, 4), sticky="W")
                        self.output_3.grid(row=4, column=1, pady=(4, 4), sticky="E")
                        self.progress_3.grid(row=5, columnspan=2, sticky="NEW")

                class add_widgets_bot(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        # Stop Button
                        self.button_1 = ttk.Button(self, text="Stop", style="Toggle.TButton", command=stopODrive)

                        # Calibrate Button
                        self.button_2 = ttk.Button(self, text="Calibrate ODrive", style="Toggle.TButton", command=calibrateODrive)

                        # Layout
                        self.button_1.pack(fill="x", pady=(0, 5))
                        self.button_2.pack(fill="x", pady=(5, 0))

                add_widgets_top(self).pack(fill="x", side="top")
                add_widgets_bot(self).pack(fill="x", side="bottom")

        class Box_2(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text="Motors", padding=data['paddingSize']['labelFrame'])

                class add_widgets_top(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        for index in range(3):
                            self.columnconfigure(index, weight=1, uniform='1')
                        for index in range(6):
                            self.rowconfigure(index, weight=1, uniform='1', minsize=data['rowSize']['label'])

                        # Side Labels
                        self.label_1 = ttk.Label(self, text='Status')
                        self.label_2 = ttk.Label(self, text='State')
                        self.label_3 = ttk.Label(self, text='Current')
                        self.label_4 = ttk.Label(self, text='Velocity')
                        self.label_5 = ttk.Label(self, text='Temperature')

                        # M1 Display Values
                        self.label_01 = ttk.Label(self, text='M1')
                        self.output_11 = ttk.Label(self, text='-')
                        self.output_21 = ttk.Label(self, text='A')
                        self.output_31 = ttk.Label(self, text='-')
                        self.output_41 = ttk.Label(self, text='°C')
                        self.progress_1 = ttk.Progressbar(self, value=0, mode="determinate")

                        # M2 Display Values
                        self.label_02 = ttk.Label(self, text='M2')
                        self.output_12 = ttk.Label(self, text='-')
                        self.output_22 = ttk.Label(self, text='A')
                        self.output_32 = ttk.Label(self, text='-')
                        self.output_42 = ttk.Label(self, text='°C')
                        self.progress_2 = ttk.Progressbar(self, value=0, mode="determinate")

                        # Layout Column 1
                        self.label_1.grid(row=0, column=0, padx=(0, 4), sticky="WE")
                        self.label_2.grid(row=1, column=0, padx=(0, 4), sticky="WE")
                        self.label_3.grid(row=2, column=0, padx=(0, 4), sticky="WE")
                        self.label_4.grid(row=3, column=0, padx=(0, 4), sticky="WE")
                        self.label_5.grid(row=4, column=0, padx=(0, 4), sticky="WE")

                        # Layout Column 2
                        self.label_01.grid(row=0, column=1, padx=(4, 4), sticky="E")
                        self.output_11.grid(row=1, column=1, padx=(4, 4), sticky="E")
                        self.output_21.grid(row=2, column=1, padx=(4, 4), sticky="E")
                        self.output_31.grid(row=3, column=1, padx=(4, 4), sticky="E")
                        self.output_41.grid(row=4, column=1, padx=(4, 4), sticky="E")
                        self.progress_1.grid(row=5, column=1, padx=(4, 4), sticky="NEW")

                        # Layout Column 3
                        self.label_02.grid(row=0, column=2, padx=(4, 0), sticky="E")
                        self.output_12.grid(row=1, column=2, padx=(4, 0), sticky="E")
                        self.output_22.grid(row=2, column=2, padx=(4, 0), sticky="E")
                        self.output_32.grid(row=3, column=2, padx=(4, 0), sticky="E")
                        self.output_42.grid(row=4, column=2, padx=(4, 0), sticky="E")
                        self.progress_2.grid(row=5, column=2, padx=(4, 0), sticky="NEW")

                class add_widgets_bot(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        for index in range(3):
                            self.columnconfigure(index, weight=1, uniform='1')

                        # Calibrate
                        self.button_1 = ttk.Button(self, style="Toggle.TButton", text="Calibrate Both", command=calibrateM1)
                        self.button_2 = ttk.Button(self, style="Toggle.TButton", text="Calibrate M1", command=calibrateM2)
                        self.button_3 = ttk.Button(self, style="Toggle.TButton", text="Calibrate M2", command=calibrateBoth)

                        # Layout
                        self.button_1.grid(row=0, column=0, padx=(0, 4), sticky="EW")
                        self.button_2.grid(row=0, column=1, padx=(4, 4), sticky="EW")
                        self.button_3.grid(row=0, column=2, padx=(4, 0), sticky="EW")

                add_widgets_top(self).pack(fill="x", side="top")
                add_widgets_bot(self).pack(fill="x", side="bottom")

        class Box_3(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text="Dashboard", padding=data['paddingSize']['labelFrame'])

                for index in range(5):
                    self.columnconfigure(index, weight=1, uniform='1')
                for index in range(5):
                    self.rowconfigure(index, weight=1, uniform='1', minsize=data['rowSize']['label'])

                self.add_widgets()

            def add_widgets(self):
                # System Labels
                self.system_label_0 = ttk.Label(self, text='System')
                self.system_label_1 = ttk.Label(self, text='RPI')
                self.system_label_2 = ttk.Label(self, text='NANO')
                self.system_label_3 = ttk.Label(self, text='ODRIVE')
                self.system_label_4 = ttk.Label(self, text='ARDUINO')

                # Status Labels
                self.status_label_0 = ttk.Label(self, text='Status')
                self.status_label_1 = ttk.Label(self, text='-')
                self.status_label_2 = ttk.Label(self, text='-')
                self.status_label_3 = ttk.Label(self, text='-')
                self.status_label_4 = ttk.Label(self, text='-')

                # Side Labels
                self.label_0 = ttk.Label(self, text='ODrive')
                self.label_1 = ttk.Label(self, text='Axis')
                self.label_2 = ttk.Label(self, text='Motor')
                self.label_3 = ttk.Label(self, text='Controller')
                self.label_4 = ttk.Label(self, text='Encoder')

                # Axis 1 Display Values
                self.label_01 = ttk.Label(self, text='Left')
                self.output_11 = ttk.Label(self, text='-')
                self.output_21 = ttk.Label(self, text='-')
                self.output_31 = ttk.Label(self, text='-')
                self.output_41 = ttk.Label(self, text='-')

                # Axis 2 Display Values
                self.label_02 = ttk.Label(self, text='Right')
                self.output_12 = ttk.Label(self, text='-')
                self.output_22 = ttk.Label(self, text='-')
                self.output_32 = ttk.Label(self, text='-')
                self.output_42 = ttk.Label(self, text='-')

                # System Status Layout
                self.system_label_0.grid(row=0, column=0, padx=(0, 4), sticky="EW")
                self.system_label_1.grid(row=1, column=0, padx=(0, 4), sticky="EW")
                self.system_label_2.grid(row=2, column=0, padx=(0, 4), sticky="EW")
                self.system_label_3.grid(row=3, column=0, padx=(0, 4), sticky="EW")
                self.system_label_4.grid(row=4, column=0, padx=(0, 4), sticky="EW")

                self.status_label_0.grid(row=0, column=1, padx=(4, 0), sticky="W")
                self.status_label_1.grid(row=1, column=1, padx=(4, 0), sticky="W")
                self.status_label_2.grid(row=2, column=1, padx=(4, 0), sticky="W")
                self.status_label_3.grid(row=3, column=1, padx=(4, 0), sticky="W")
                self.status_label_4.grid(row=4, column=1, padx=(4, 0), sticky="W")

                # Left & Right - Odrive Status Layout
                self.label_0.grid(row=0, column=2, padx=(0, 4), sticky="EW")
                self.label_1.grid(row=1, column=2, padx=(0, 4), sticky="EW")
                self.label_2.grid(row=2, column=2, padx=(0, 4), sticky="EW")
                self.label_3.grid(row=3, column=2, padx=(0, 4), sticky="EW")
                self.label_4.grid(row=4, column=2, padx=(0, 4), sticky="EW")

                self.label_01.grid(row=0, column=3, padx=(4, 4), sticky="EW")
                self.output_11.grid(row=1, column=3, padx=(4, 4), sticky="EW")
                self.output_21.grid(row=2, column=3, padx=(4, 4), sticky="EW")
                self.output_31.grid(row=3, column=3, padx=(4, 4), sticky="EW")
                self.output_41.grid(row=4, column=3, padx=(4, 4), sticky="EW")

                self.label_02.grid(row=0, column=4, padx=(4, 0), sticky="EW")
                self.output_12.grid(row=1, column=4, padx=(4, 0), sticky="EW")
                self.output_22.grid(row=2, column=4, padx=(4, 0), sticky="EW")
                self.output_32.grid(row=3, column=4, padx=(4, 0), sticky="EW")
                self.output_42.grid(row=4, column=4, padx=(4, 0), sticky="EW")

        class Box_4(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text="Battery", padding=data['paddingSize']['labelFrame'])

                for index in range(2):
                    self.columnconfigure(index, weight=1, uniform='1')
                for index in range(2):
                    self.rowconfigure(index, weight=1, uniform='1', minsize=data['rowSize']['label'])
                self.rowconfigure(2, weight=1, minsize=data['rowSize']['progressBar'])

                self.add_widgets()

            def add_widgets(self):
                # Battery
                self.label_1 = ttk.Label(self, text='Voltage')
                self.label_2 = ttk.Label(self, text='Temperature')
                self.progress_2 = ttk.Progressbar(self, value=0, mode="determinate")

                # Battery Display Values
                self.output_1 = ttk.Label(self, text='V')
                self.output_2 = ttk.Label(self, text='°C')

                # Layout
                self.label_1.grid(row=0, column=0, sticky="WE")
                self.label_2.grid(row=1, column=0, sticky="WE")
                self.output_1.grid(row=0, column=1, sticky="E")
                self.output_2.grid(row=1, column=1, sticky="E")
                self.progress_2.grid(row=2, column=0, columnspan=2, sticky="NEW")

        class Box_5(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text="Speed & Steering", padding=data['paddingSize']['labelFrame'])

                class add_widgets_top(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        for index in range(2):
                            self.columnconfigure(index, weight=1, uniform='1')
                        for index in (0, 2):
                            self.rowconfigure(index, weight=1, minsize=data['rowSize']['label'])
                        for index in (1, 3):
                            self.rowconfigure(index, weight=1, minsize=data['rowSize']['progressBar'])

                        # Speed
                        self.label_speed = ttk.Label(self, text='Speed')
                        self.output_speed = ttk.Label(self, text='-')
                        self.progress_speed = ttk.Progressbar(self, value=50, mode="indeterminate")

                        # Steering
                        self.label_steering = ttk.Label(self, text='Steering')
                        self.output_steering = ttk.Label(self, text='-')
                        self.progress_steering = ttk.Progressbar(self, value=50, mode="indeterminate")

                        # Layout
                        self.label_speed.grid(row=0, column=0, sticky="WE")
                        self.output_speed.grid(row=0, column=1, sticky="E")
                        self.progress_speed.grid(row=1, column=0, columnspan=2, sticky="NEW")

                        self.label_steering.grid(row=2, column=0, sticky="WE")
                        self.output_steering.grid(row=2, column=1, sticky="E")
                        self.progress_steering.grid(row=3, column=0, columnspan=2, sticky="NEW")

                class add_widgets_bot(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        # Steering Button
                        self.button_steering = ttk.Button(self, text="Calibrate Steering", style="Toggle.TButton", command=calibrateSteering)

                        # Layout
                        self.button_steering.pack(fill="x", pady=(8, 0))

                add_widgets_top(self).pack(fill="x", side="top")
                add_widgets_bot(self).pack(fill="x", side="bottom")

        class Box_6(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text="Controls", padding=data['paddingSize']['labelFrame'])

                class add_widgets_left(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        for index in range(0, 6, 2):
                            self.columnconfigure(index, weight=1, uniform='1', minsize=36)
                        for index in range(1, 5, 2):
                            self.columnconfigure(index, weight=1, minsize=6)
                        for index in range(0, 3, 2):
                            self.rowconfigure(index, weight=1, uniform='1', minsize=36)
                        self.rowconfigure(1, weight=1, minsize=6)

                        # Keyboard Buttons
                        self.label_key_w = ttk.Button(self, style="Toggle.TButton", text="W", command=moveAccelerate)
                        self.label_key_a = ttk.Button(self, style="Toggle.TButton", text="A", command=moveSteerLeft)
                        self.label_key_s = ttk.Button(self, style="Toggle.TButton", text="S", command=moveDecelerate)
                        self.label_key_d = ttk.Button(self, style="Toggle.TButton", text="D", command=moveSteerRight)

                        # Layout
                        self.label_key_w.grid(row=0, column=2, sticky="NSEW")
                        self.label_key_a.grid(row=2, column=0, sticky="NSEW")
                        self.label_key_s.grid(row=2, column=2, sticky="NSEW")
                        self.label_key_d.grid(row=2, column=4, sticky="NSEW")
                        self.bindings()

                    def bindings(self):
                        root.bind("<KeyPress-w>", lambda event: keyPress(self.label_key_w, True))
                        root.bind("<KeyRelease-w>", lambda event: keyPress(self.label_key_w, False))
                        root.bind("<KeyPress-a>", lambda event: keyPress(self.label_key_a, True))
                        root.bind("<KeyRelease-a>", lambda event: keyPress(self.label_key_a, False))
                        root.bind("<KeyPress-s>", lambda event: keyPress(self.label_key_s, True))
                        root.bind("<KeyRelease-s>", lambda event: keyPress(self.label_key_s, False))
                        root.bind("<KeyPress-d>", lambda event: keyPress(self.label_key_d, True))
                        root.bind("<KeyRelease-d>", lambda event: keyPress(self.label_key_d, False))

                class add_widgets_right(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        self.columnconfigure(0, minsize=108)
                        for index in range(0, 3, 2):
                            self.rowconfigure(index, weight=1, uniform='1', minsize=36)
                        self.rowconfigure(1, minsize=6)

                        # Keyboard Buttons
                        self.label_key_x = ttk.Button(self, style="Toggle.TButton", text="X", command=moveBrake)

                        # Layout
                        self.label_key_x.grid(row=2, sticky="NSEW")
                        self.bindings()

                    def bindings(self):
                        root.bind("<KeyPress-x>", lambda event: keyPress(self.label_key_x, True))
                        root.bind("<KeyRelease-x>", lambda event: keyPress(self.label_key_x, False))

                add_widgets_left(self).pack(side="left")
                add_widgets_right(self).pack(side="right")

        # Set Layout UI Boxes
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        for index in (1, 2, 3):
            self.rowconfigure(index, weight=1)

        Menu_Bar(self).grid(row=0, columnspan=3, sticky="EW")
        Box_1(self).grid(row=1, rowspan=2, column=0, padx=(0, 4), pady=(4, 4), sticky="NSEW")
        Box_2(self).grid(row=1, rowspan=2, column=1, padx=(4, 4), pady=(4, 4), sticky="NSEW")
        Box_3(self).grid(row=3, column=0, columnspan=2, padx=(0, 4), pady=(4, 0), sticky="NSEW")
        Box_4(self).grid(row=1, column=2, padx=(4, 0), pady=(4, 4), sticky="NSEW")
        Box_5(self).grid(row=2, column=2, padx=(4, 0), pady=(4, 4), sticky="NSEW")
        Box_6(self).grid(row=3, column=2, padx=(4, 0), pady=(4, 0), sticky="NSEW")


class Tab2(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        class Menu_Bar(ttk.Frame):
            def __init__(self, parent):
                super().__init__(parent, padding=data['paddingSize']['frame'])

                # Camera Switch
                self.toggle_switch_1 = IntVar()
                self.switch_1 = ttk.Checkbutton(self, style="Switch.TCheckbutton", variable=self.toggle_switch_1, text="Show Cam On Display", command=lambda: switchCamera(OpenCV(parent), self.toggle_switch_1))

                # Quit GUI
                self.button_1 = ttk.Button(self, style="Toggle.TButton", text="❌", command=lambda: systemShutdown(root))

                # Layout
                self.switch_1.pack(padx=(0, 4), side='left')
                self.button_1.pack(padx=(4, 0), side='right')
                self.button_1.shouldToggle = False
                self.bindings()

            def bindings(self):
                root.bind("<KeyPress-Escape>", lambda event: keyPress(self.button_1, True))
                root.bind("<KeyRelease-Escape>", lambda event: keyPress(self.button_1, False))

        class OpenCV(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='CAM', padding=data['paddingSize']['labelFrame'])

                self.label = ttk.Label(self)
                self.label.pack()

                cap = cv2.VideoCapture(0)

                # Define function to show frame
                def showFrames():
                    # Get the latest frame and convert into Image
                    cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(cv2image)

                    # Convert image to PhotoImage
                    self.label.imgtk = ImageTk.PhotoImage(image=img)
                    self.label.configure(image=self.label.imgtk)

                    # Repeat after an interval to capture continiously
                    self.label.after(50, showFrames)

                showFrames()

        Menu_Bar(self).pack(fill='x', side='top')
        OpenCV(self).pack(fill='x', side='top')


class Tab3(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)


class App(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create Notebook & Frames (Tabs)
        self.notebook = ttk.Notebook(self, style='TNotebook')
        self.tab_1 = ttk.Frame(self.notebook, padding=data['paddingSize']['appFrame'])
        self.tab_2 = ttk.Frame(self.notebook, padding=data['paddingSize']['appFrame'])
        self.tab_3 = ttk.Frame(self.notebook, padding=data['paddingSize']['appFrame'])

        # Add Tabs in Notebook
        self.notebook.add(self.tab_1, text='Home')
        self.notebook.add(self.tab_2, text='Cam')
        self.notebook.add(self.tab_3, text='Graph')
        self.notebook.pack(expand=1, fill='both')

        # Displaying
        Tab1(self.tab_1).pack(expand=1, fill='both')
        Tab2(self.tab_2).pack(expand=1, fill='both')
        Tab3(self.tab_3).pack(expand=1, fill='both')

        # Initialise All Buttons to be Disabled (Except Power & Close Button)
        toggleAllChildren(self, False)


def main():
    global root
    root = tk.Tk()

    # Configure the root window
    root.title('Title')
    root.geometry('1000x600')
    w = data['windowSize']['width']
    h = data['windowSize']['height']

    # Calculate Starting X and Y coordinates for Window
    x = (root.winfo_screenwidth() / 2) - (w / 2)
    y = (root.winfo_screenheight() / 2) - (h / 2)

    # Open window at the center of the screen and is borderless
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.overrideredirect(0)

    # Set theme
    sv_ttk.set_theme('dark')

    # Set Widget Styles
    style = ttk.Style(root)
    style.configure('.', font=(data['font']['family'], data['font']['size']))
    style.configure('T.Label', font=(data['font']['family'], data['font']['size']))

    # Set Global Fonts
    root.font = font.Font(family=data['font']['family'], size=data['font']['size'])
    root.option_add("*Font", root.font)

    App(root).pack(expand=1, fill='both')
    root.mainloop()


if __name__ == "__main__":
    main()
