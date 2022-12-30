import tkinter as tk
import sv_ttk as sv
from tkinter import ttk, font, IntVar

# Time
import time
startTime = time.time()

# Read JSON file and Store Data
import json
with open('./config.json', 'r') as file:
    data = json.load(file)

# Import Python Files
from Functions.LiveButtons import *
from Functions.LiveDashboard import *
from Functions.LiveCam import *
from Functions.LiveGraph import *
from Functions.LiveLabels import registerLiveLabel, registerLiveBar, updateLiveLabel


class Tab1(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        class Menu_Bar(ttk.Frame):
            def __init__(self, parent):
                super().__init__(parent, padding=data['paddingSize']['frame'])

                # Toggle GUI Control Switch
                root.toggle_switch_0 = IntVar()
                self.switch_0 = ttk.Checkbutton(self, style='Switch.TCheckbutton', variable=root.toggle_switch_0, text='GUI', command=lambda: systemGUI(root, root.toggle_switch_0))
                self.switch_0.shouldToggle = False

                # Toggle Monitor Switch
                self.toggle_switch_1 = IntVar()
                self.switch_1 = ttk.Checkbutton(self, style='Switch.TCheckbutton', variable=self.toggle_switch_1, text='Monitor', command=lambda: switchODrive(root, self.toggle_switch_1))

                # Toggle Control Loop Switch
                self.toggle_switch_2 = IntVar()
                self.switch_2 = ttk.Checkbutton(self, style='Switch.TCheckbutton', variable=self.toggle_switch_2, text='Control Loop', command=lambda: switchControlLoop(self.toggle_switch_2))

                # Quit GUI
                self.button_1 = ttk.Button(self, style='Toggle.TButton', text='❌', command=lambda: systemShutdown(root))
                self.button_1.shouldToggle = False

                # Layout
                self.switch_0.pack(padx=(0, 4), side='left')
                self.switch_1.pack(padx=(4, 4), side='left')
                self.switch_2.pack(padx=(4, 4), side='left')
                self.button_1.pack(padx=(4, 0), side='right')

                self.bindings()

            def bindings(self):
                root.bind('<KeyPress-Escape>', lambda event: keyPress(self.button_1, True))
                root.bind('<KeyRelease-Escape>', lambda event: keyPress(self.button_1, False))

        class Box_1(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='ODrive', padding=data['paddingSize']['labelFrame'])

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
                        self.progress_1 = ttk.Progressbar(self, mode='determinate')

                        # Live Labels & Bars
                        registerLiveLabel('M1Temp', self.output_1)
                        registerLiveBar('M1TempBar', self.progress_1)

                        # MOSFET M2
                        self.label_2 = ttk.Label(self, text='MOSFET M2')
                        self.output_2 = ttk.Label(self, text='°C')    
                        self.progress_2 = ttk.Progressbar(self, mode='determinate')
                        
                        # Live Labels & Bars
                        registerLiveLabel('M2Temp', self.output_2)
                        registerLiveBar('M2TempBar', self.progress_2)
                        
                        # MOSFET BRAKES
                        self.label_3 = ttk.Label(self, text='MOSFET BRAKES')
                        self.output_3 = ttk.Label(self, text='°C')
                        self.progress_3 = ttk.Progressbar(self, mode='determinate')
                        
                        # Live Labels & Bars
                        registerLiveLabel('brakesTemp', self.output_3)
                        registerLiveBar('brakesTempBar', self.progress_3)

                        # Layout
                        self.label_1.grid(row=0, column=0, pady=(4, 4), sticky='W')
                        self.output_1.grid(row=0, column=1, pady=(4, 4), sticky='E')
                        self.progress_1.grid(row=1, columnspan=2, sticky='NEW')

                        self.label_2.grid(row=2, column=0, pady=(4, 4), sticky='W')
                        self.output_2.grid(row=2, column=1, pady=(4, 4), sticky='E')
                        self.progress_2.grid(row=3, columnspan=2, sticky='NEW')

                        self.label_3.grid(row=4, column=0, pady=(4, 4), sticky='W')
                        self.output_3.grid(row=4, column=1, pady=(4, 4), sticky='E')
                        self.progress_3.grid(row=5, columnspan=2, sticky='NEW')

                class add_widgets_bot(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        # Stop Button
                        self.button_1 = ttk.Button(self, text='Stop', style='Toggle.TButton', command=stopODrive)

                        # Calibrate Button
                        self.button_2 = ttk.Button(self, text='Calibrate ODrive', style='Toggle.TButton', command=lambda: calibrateControls('ODrive'))

                        # Layout
                        self.button_1.pack(fill='x', pady=(0, 4))
                        self.button_2.pack(fill='x', pady=(4, 0))

                add_widgets_top(self).pack(fill='x', side='top')
                add_widgets_bot(self).pack(fill='x', side='bottom')

        class Box_2(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Motors', padding=data['paddingSize']['labelFrame'])

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
                        self.progress_1 = ttk.Progressbar(self, mode='determinate')
                        
                        # Live Labels & Bars
                        registerLiveLabel('M1State', self.output_11)
                        registerLiveLabel('M1Current', self.output_21)
                        registerLiveLabel('M1Velocity', self.output_31)
                        registerLiveLabel('M1Temp', self.output_41)
                        registerLiveBar('M1TempBar', self.progress_1)

                        # M2 Display Values
                        self.label_02 = ttk.Label(self, text='M2')
                        self.output_12 = ttk.Label(self, text='-')
                        self.output_22 = ttk.Label(self, text='A')
                        self.output_32 = ttk.Label(self, text='-')
                        self.output_42 = ttk.Label(self, text='°C')
                        self.progress_2 = ttk.Progressbar(self, mode='determinate')
                        
                        # Live Labels & Bars
                        registerLiveLabel('M2State', self.output_12)
                        registerLiveLabel('M2Current', self.output_22)
                        registerLiveLabel('M2Velocity', self.output_32)
                        registerLiveLabel('M2Temp', self.output_42)
                        registerLiveBar('M2TempBar', self.progress_2)

                        # Layout Column 1
                        self.label_1.grid(row=0, column=0, padx=(0, 4), sticky='EW')
                        self.label_2.grid(row=1, column=0, padx=(0, 4), sticky='EW')
                        self.label_3.grid(row=2, column=0, padx=(0, 4), sticky='EW')
                        self.label_4.grid(row=3, column=0, padx=(0, 4), sticky='EW')
                        self.label_5.grid(row=4, column=0, padx=(0, 4), sticky='EW')

                        # Layout Column 2
                        self.label_01.grid(row=0, column=1, padx=(4, 4), sticky='E')
                        self.output_11.grid(row=1, column=1, padx=(4, 4), sticky='E')
                        self.output_21.grid(row=2, column=1, padx=(4, 4), sticky='E')
                        self.output_31.grid(row=3, column=1, padx=(4, 4), sticky='E')
                        self.output_41.grid(row=4, column=1, padx=(4, 4), sticky='E')
                        self.progress_1.grid(row=5, column=1, padx=(4, 4), sticky='NEW')

                        # Layout Column 3
                        self.label_02.grid(row=0, column=2, padx=(4, 0), sticky='E')
                        self.output_12.grid(row=1, column=2, padx=(4, 0), sticky='E')
                        self.output_22.grid(row=2, column=2, padx=(4, 0), sticky='E')
                        self.output_32.grid(row=3, column=2, padx=(4, 0), sticky='E')
                        self.output_42.grid(row=4, column=2, padx=(4, 0), sticky='E')
                        self.progress_2.grid(row=5, column=2, padx=(4, 0), sticky='NEW')

                class add_widgets_bot(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        for index in range(3):
                            self.columnconfigure(index, weight=1, uniform='1')

                        # Calibrate
                        self.button_1 = ttk.Button(self, style='Toggle.TButton', text='Calibrate Both', command=lambda: calibrateControls('M1'))
                        self.button_2 = ttk.Button(self, style='Toggle.TButton', text='Calibrate M1', command=lambda: calibrateControls('M2'))
                        self.button_3 = ttk.Button(self, style='Toggle.TButton', text='Calibrate M2', command=lambda: calibrateControls('Both'))

                        # Layout
                        self.button_1.grid(row=0, column=0, padx=(0, 4), sticky='EW')
                        self.button_2.grid(row=0, column=1, padx=(4, 4), sticky='EW')
                        self.button_3.grid(row=0, column=2, padx=(4, 0), sticky='EW')

                add_widgets_top(self).pack(fill='x', side='top')
                add_widgets_bot(self).pack(fill='x', side='bottom')

        class Box_3(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Dashboard', padding=data['paddingSize']['labelFrame'])

                for index in range(5):
                    self.columnconfigure(index, weight=1, uniform='1')
                for index in range(5):
                    self.rowconfigure(index, weight=1, uniform='1', minsize=data['rowSize']['label'])

                self.add_widgets()

            def add_widgets(self):
                # System Labels
                self.system_label_0 = ttk.Label(self, text='System')
                self.system_label_1 = ttk.Label(self, text='RPI')
                self.system_label_2 = ttk.Label(self, text='JETSON')
                self.system_label_3 = ttk.Label(self, text='ODRIVE')
                self.system_label_4 = ttk.Label(self, text='ARDUINO')

                # Status Labels
                self.status_label_0 = ttk.Label(self, text='Status')
                self.status_label_1 = ttk.Label(self, text='-')
                self.status_label_2 = ttk.Label(self, text='-')
                self.status_label_3 = ttk.Label(self, text='-')
                self.status_label_4 = ttk.Label(self, text='-')
                
                # Live Labels & Bars
                registerLiveLabel('RPIStatus', self.status_label_1)
                registerLiveLabel('JETSONStatus', self.status_label_2)
                registerLiveLabel('ODRIVEStatus', self.status_label_3)
                registerLiveLabel('ARDUINOStatus', self.status_label_4)

                # Side Labels
                self.label_0 = ttk.Label(self, text='Error')
                self.label_1 = ttk.Label(self, text='Axis')
                self.label_2 = ttk.Label(self, text='Motor')
                self.label_3 = ttk.Label(self, text='Controller')
                self.label_4 = ttk.Label(self, text='Encoder')

                # Axis 1 Display Values
                self.label_01 = ttk.Label(self, text='Axis 0')
                self.output_11 = ttk.Label(self, text='-')
                self.output_21 = ttk.Label(self, text='-')
                self.output_31 = ttk.Label(self, text='-')
                self.output_41 = ttk.Label(self, text='-')

                # Live Labels & Bars
                registerLiveLabel('A1Error', self.output_11)
                registerLiveLabel('A1MotorError', self.output_21)
                registerLiveLabel('A1ControllerError', self.output_31)
                registerLiveLabel('A1EncoderError', self.output_41)

                # Axis 2 Display Values
                self.label_02 = ttk.Label(self, text='Axis 1')
                self.output_12 = ttk.Label(self, text='-')
                self.output_22 = ttk.Label(self, text='-')
                self.output_32 = ttk.Label(self, text='-')
                self.output_42 = ttk.Label(self, text='-')
                
                # Live Labels & Bars
                registerLiveLabel('A2Error', self.output_12)
                registerLiveLabel('A2MotorError', self.output_22)
                registerLiveLabel('A2ControllerError', self.output_32)
                registerLiveLabel('A2EncoderError', self.output_42)

                # System Status Layout
                self.system_label_0.grid(row=0, column=0, padx=(0, 4), sticky='EW')
                self.system_label_1.grid(row=1, column=0, padx=(0, 4), sticky='EW')
                self.system_label_2.grid(row=2, column=0, padx=(0, 4), sticky='EW')
                self.system_label_3.grid(row=3, column=0, padx=(0, 4), sticky='EW')
                self.system_label_4.grid(row=4, column=0, padx=(0, 4), sticky='EW')

                self.status_label_0.grid(row=0, column=1, padx=(4, 0), sticky='W')
                self.status_label_1.grid(row=1, column=1, padx=(4, 0), sticky='W')
                self.status_label_2.grid(row=2, column=1, padx=(4, 0), sticky='W')
                self.status_label_3.grid(row=3, column=1, padx=(4, 0), sticky='W')
                self.status_label_4.grid(row=4, column=1, padx=(4, 0), sticky='W')

                # Left & Right - Odrive Status Layout
                self.label_0.grid(row=0, column=2, padx=(0, 4), sticky='EW')
                self.label_1.grid(row=1, column=2, padx=(0, 4), sticky='EW')
                self.label_2.grid(row=2, column=2, padx=(0, 4), sticky='EW')
                self.label_3.grid(row=3, column=2, padx=(0, 4), sticky='EW')
                self.label_4.grid(row=4, column=2, padx=(0, 4), sticky='EW')

                self.label_01.grid(row=0, column=3, padx=(4, 4), sticky='EW')
                self.output_11.grid(row=1, column=3, padx=(4, 4), sticky='EW')
                self.output_21.grid(row=2, column=3, padx=(4, 4), sticky='EW')
                self.output_31.grid(row=3, column=3, padx=(4, 4), sticky='EW')
                self.output_41.grid(row=4, column=3, padx=(4, 4), sticky='EW')

                self.label_02.grid(row=0, column=4, padx=(4, 0), sticky='EW')
                self.output_12.grid(row=1, column=4, padx=(4, 0), sticky='EW')
                self.output_22.grid(row=2, column=4, padx=(4, 0), sticky='EW')
                self.output_32.grid(row=3, column=4, padx=(4, 0), sticky='EW')
                self.output_42.grid(row=4, column=4, padx=(4, 0), sticky='EW')

        class Box_4(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Battery', padding=data['paddingSize']['labelFrame'])

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

                # Battery Display Values
                self.output_1 = ttk.Label(self, text='V')
                self.output_2 = ttk.Label(self, text='°C')
                self.progress_2 = ttk.Progressbar(self, mode='determinate')
                
                # Live Labels & Bars
                registerLiveLabel('batteryVoltage', self.output_1)
                registerLiveLabel('batteryTemp', self.output_2)
                registerLiveBar('batteryTempBar', self.progress_2)

                # Layout
                self.label_1.grid(row=0, column=0, sticky='EW')
                self.label_2.grid(row=1, column=0, sticky='EW')
                self.output_1.grid(row=0, column=1, sticky='E')
                self.output_2.grid(row=1, column=1, sticky='E')
                self.progress_2.grid(row=2, column=0, columnspan=2, sticky='NEW')

        class Box_5(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Speed & Steering', padding=data['paddingSize']['labelFrame'])

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
                        self.label_1 = ttk.Label(self, text='Speed')
                        self.output_1 = ttk.Label(self, text='-')
                        self.progress_1 = ttk.Progressbar(self, value=50, mode='indeterminate')
                        
                        # Live Labels & Bars
                        registerLiveLabel('speed', self.output_1)
                        registerLiveBar('speedBar', self.progress_1)

                        # Steering
                        self.label_2 = ttk.Label(self, text='Steering')
                        self.output_2 = ttk.Label(self, text='-')
                        self.progress_2 = ttk.Progressbar(self, value=50, mode='indeterminate')
                        
                        # Live Labels & Bars
                        registerLiveLabel('steerAngle', self.output_2)
                        registerLiveBar('steerAngleBar', self.progress_2)

                        # Layout
                        self.label_1.grid(row=0, column=0, sticky='EW')
                        self.output_1.grid(row=0, column=1, sticky='E')
                        self.progress_1.grid(row=1, column=0, columnspan=2, sticky='NEW')
                        self.label_2.grid(row=2, column=0, sticky='EW')
                        self.output_2.grid(row=2, column=1, sticky='E')
                        self.progress_2.grid(row=3, column=0, columnspan=2, sticky='NEW')

                class add_widgets_bot(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        # Steering Button
                        self.button_steering = ttk.Button(self, text='Calibrate Steering', style='Toggle.TButton', command=lambda: calibrateControls('steering'))

                        # Layout
                        self.button_steering.pack(fill='x', pady=(8, 0))

                add_widgets_top(self).pack(fill='x', side='top')
                add_widgets_bot(self).pack(fill='x', side='bottom')

        class Box_6(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Controls', padding=data['paddingSize']['labelFrame'])
                
                if data['controlSettings']['controlType'] == 'keyboard':

                    class add_widgets_left(ttk.Frame):
                        def __init__(self, parent):
                            super().__init__(parent, padding=data['paddingSize']['frame'])

                            for index in range(0, 6, 2):
                                self.columnconfigure(index, weight=1, uniform='1', minsize=36)
                            for index in range(1, 5, 2):
                                self.columnconfigure(index, weight=0, minsize=6)
                            for index in range(0, 3, 2):
                                self.rowconfigure(index, weight=1, uniform='1', minsize=36)
                            self.rowconfigure(1, weight=1, minsize=6)

                            # Keyboard Buttons
                            self.label_key_w = ttk.Button(self, style='Toggle.TButton', text='W', command=lambda: movementControls('up'))
                            self.label_key_a = ttk.Button(self, style='Toggle.TButton', text='A', command=lambda: movementControls('down'))
                            self.label_key_s = ttk.Button(self, style='Toggle.TButton', text='S', command=lambda: movementControls('left'))
                            self.label_key_d = ttk.Button(self, style='Toggle.TButton', text='D', command=lambda: movementControls('right'))

                            # Layout
                            self.label_key_w.grid(row=0, column=2, sticky='NSEW')
                            self.label_key_a.grid(row=2, column=0, sticky='NSEW')
                            self.label_key_s.grid(row=2, column=2, sticky='NSEW')
                            self.label_key_d.grid(row=2, column=4, sticky='NSEW')

                            self.bindings()

                        def bindings(self):
                            root.bind('<KeyPress-w>', lambda event: keyPress(self.label_key_w, True))
                            root.bind('<KeyRelease-w>', lambda event: keyPress(self.label_key_w, False))
                            root.bind('<KeyPress-a>', lambda event: keyPress(self.label_key_a, True))
                            root.bind('<KeyRelease-a>', lambda event: keyPress(self.label_key_a, False))
                            root.bind('<KeyPress-s>', lambda event: keyPress(self.label_key_s, True))
                            root.bind('<KeyRelease-s>', lambda event: keyPress(self.label_key_s, False))
                            root.bind('<KeyPress-d>', lambda event: keyPress(self.label_key_d, True))
                            root.bind('<KeyRelease-d>', lambda event: keyPress(self.label_key_d, False))

                    class add_widgets_right(ttk.Frame):
                        def __init__(self, parent):
                            super().__init__(parent, padding=data['paddingSize']['frame'])

                            self.columnconfigure(0, weight=1, uniform='1', minsize=36*2)
                            for index in range(0, 3, 2):
                                self.rowconfigure(index, weight=1, uniform='1', minsize=36)
                            self.rowconfigure(1, minsize=6)

                            # Keyboard Buttons
                            self.label_key_x = ttk.Button(self, style='Toggle.TButton', text='X', command=lambda: movementControls('brake'))

                            # Layout
                            self.label_key_x.grid(row=2, sticky='NSEW')

                            self.bindings()

                        def bindings(self):
                            root.bind('<KeyPress-x>', lambda event: keyPress(self.label_key_x, True))
                            root.bind('<KeyRelease-x>', lambda event: keyPress(self.label_key_x, False))

                    add_widgets_left(self).pack(side='left')
                    add_widgets_right(self).pack(side='right')
                    
                if data['controlSettings']['controlType'] == 'controller':
                    
                    class add_widgets_top(ttk.Frame):
                        def __init__(self, parent):
                            super().__init__(parent, padding=data['paddingSize']['frame'])
                            
                            # Controller Buttons
                            self.label_key_lt = ttk.Button(self, style='Toggle.TButton', text='LT', command=lambda: movementControls('up'))
                            self.label_key_lb = ttk.Button(self, style='Toggle.TButton', text='LB', command=lambda: movementControls('up'))
                            self.label_key_rt = ttk.Button(self, style='Toggle.TButton', text='RT', command=lambda: movementControls('up'))
                            self.label_key_rb = ttk.Button(self, style='Toggle.TButton', text='RB', command=lambda: movementControls('up'))
                            
                            # # Layout
                            self.label_key_lt.pack(padx=(0, 2), side='left')
                            self.label_key_lb.pack(padx=(2, 0), side='left')
                            self.label_key_rt.pack(padx=(2, 0), side='right')
                            self.label_key_rb.pack(padx=(0, 2), side='right')
                        
                    class add_widgets_left(ttk.Frame):
                        def __init__(self, parent):
                            super().__init__(parent, padding=data['paddingSize']['frame'])

                            # Keyboard Buttons
                            self.label_key_up = ttk.Button(self, style='Toggle.TButton', text='  ', command=lambda: movementControls('up'))
                            self.label_key_down = ttk.Button(self, style='Toggle.TButton', text='  ', command=lambda: movementControls('down'))
                            self.label_key_left = ttk.Button(self, style='Toggle.TButton', text='  ', command=lambda: movementControls('left'))
                            self.label_key_right = ttk.Button(self, style='Toggle.TButton', text='  ', command=lambda: movementControls('right'))

                            # Layout
                            self.label_key_left.pack(padx=(0, 3), side='left')
                            self.label_key_right.pack(padx=(3, 0), side='right')
                            self.label_key_up.pack(pady=(0, 2), side='top')
                            self.label_key_down.pack(pady=(2, 0), side='top')
                            
                            self.bindings()

                        def bindings(self):
                            root.bind('<KeyPress-w>', lambda event: keyPress(self.label_key_up, True))
                            root.bind('<KeyRelease-w>', lambda event: keyPress(self.label_key_up, False))
                            root.bind('<KeyPress-a>', lambda event: keyPress(self.label_key_left, True))
                            root.bind('<KeyRelease-a>', lambda event: keyPress(self.label_key_left, False))
                            root.bind('<KeyPress-s>', lambda event: keyPress(self.label_key_down, True))
                            root.bind('<KeyRelease-s>', lambda event: keyPress(self.label_key_down, False))
                            root.bind('<KeyPress-d>', lambda event: keyPress(self.label_key_right, True))
                            root.bind('<KeyRelease-d>', lambda event: keyPress(self.label_key_right, False))

                    class add_widgets_right(ttk.Frame):
                        def __init__(self, parent):
                            super().__init__(parent, padding=data['paddingSize']['frame'])

                            # Keyboard Buttons
                            self.label_key_x = ttk.Button(self, style='Toggle.TButton', text='  ', command=lambda: movementControls('up'))
                            self.label_key_y = ttk.Button(self, style='Toggle.TButton', text='  ', command=lambda: movementControls('down'))
                            self.label_key_a = ttk.Button(self, style='Toggle.TButton', text='  ', command=lambda: movementControls('left'))
                            self.label_key_b = ttk.Button(self, style='Toggle.TButton', text='  ', command=lambda: movementControls('right'))

                            # Layout
                            self.label_key_x.pack(padx=(0, 3), side='left')
                            self.label_key_b.pack(padx=(3, 0), side='right')
                            self.label_key_y.pack(pady=(0, 2), side='top')
                            self.label_key_a.pack(pady=(2, 0), side='top')

                            self.bindings()

                        def bindings(self):
                            root.bind('<KeyPress-w>', lambda event: keyPress(self.label_key_x, True))
                            root.bind('<KeyRelease-w>', lambda event: keyPress(self.label_key_x, False))
                            root.bind('<KeyPress-a>', lambda event: keyPress(self.label_key_y, True))
                            root.bind('<KeyRelease-a>', lambda event: keyPress(self.label_key_y, False))
                            root.bind('<KeyPress-s>', lambda event: keyPress(self.label_key_a, True))
                            root.bind('<KeyRelease-s>', lambda event: keyPress(self.label_key_a, False))
                            root.bind('<KeyPress-d>', lambda event: keyPress(self.label_key_b, True))
                            root.bind('<KeyRelease-d>', lambda event: keyPress(self.label_key_b, False))

                    class add_widgets_bot(ttk.Frame):
                        def __init__(self, parent):
                            super().__init__(parent, padding=data['paddingSize']['frame'])
                            
                            # Controller Buttons
                            self.label_key_lt = ttk.Button(self, style='Toggle.TButton', text='LT', command=lambda: movementControls('up'))
                            self.label_key_lb = ttk.Button(self, style='Toggle.TButton', text='LB', command=lambda: movementControls('up'))
                            self.label_key_rt = ttk.Button(self, style='Toggle.TButton', text='RT', command=lambda: movementControls('up'))
                            self.label_key_rb = ttk.Button(self, style='Toggle.TButton', text='RB', command=lambda: movementControls('up'))
                            
                            # # Layout
                            self.label_key_lt.pack(padx=(0, 2), side='left')
                            self.label_key_lb.pack(padx=(2, 0), side='left')
                            self.label_key_rt.pack(padx=(2, 0), side='right')
                            self.label_key_rb.pack(padx=(0, 2), side='right')

                    add_widgets_top(self).pack(fill='x', side='top')
                    add_widgets_bot(self).pack(fill='x', side='bottom')
                    add_widgets_left(self).pack(side='left')
                    add_widgets_right(self).pack(side='right')

        # Set Layout UI Boxes
        self.columnconfigure(0, weight=1, uniform='1')
        self.columnconfigure(1, weight=2, uniform='1')
        self.columnconfigure(2, weight=1, uniform='1')
        for index in (1, 2, 3):
            self.rowconfigure(index, weight=1)

        Menu_Bar(self).grid(row=0, columnspan=3, sticky='EW')
        Box_1(self).grid(row=1, rowspan=2, column=0, padx=(0, 4), pady=(4, 4), sticky='NSEW')
        Box_2(self).grid(row=1, rowspan=2, column=1, padx=(4, 4), pady=(4, 4), sticky='NSEW')
        Box_3(self).grid(row=3, column=0, columnspan=2, padx=(0, 4), pady=(4, 0), sticky='NSEW')
        Box_4(self).grid(row=1, column=2, padx=(4, 0), pady=(4, 4), sticky='NSEW')
        Box_5(self).grid(row=2, column=2, padx=(4, 0), pady=(4, 4), sticky='NSEW')
        Box_6(self).grid(row=3, column=2, padx=(4, 0), pady=(4, 0), sticky='NSEW')


class Tab2(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        class Menu_Bar(ttk.Frame):
            def __init__(self, parent):
                super().__init__(parent, padding=data['paddingSize']['frame'])
                
                # Toggle GUI Control Switch
                self.switch_0 = ttk.Checkbutton(self, style='Switch.TCheckbutton', variable=root.toggle_switch_0, text='GUI', command=lambda: systemGUI(root, root.toggle_switch_0))
                self.switch_0.shouldToggle = False

                # Toggle Camera Switch
                self.toggle_switch_1 = IntVar()
                self.switch_1 = ttk.Checkbutton(self, style='Switch.TCheckbutton', variable=self.toggle_switch_1, text='Display Cam', command=lambda: switchCamera(self.master.opencv.label, self.toggle_switch_1))

                # Quit GUI
                self.button_1 = ttk.Button(self, style='Toggle.TButton', text='❌', command=lambda: systemShutdown(root))
                self.button_1.shouldToggle = False

                # Layout
                self.switch_0.pack(padx=(0, 4), side='left')
                self.switch_1.pack(padx=(0, 4), side='left')
                self.button_1.pack(padx=(4, 0), side='right')

                self.bindings()

            def bindings(self):
                root.bind('<KeyPress-Escape>', lambda event: keyPress(self.button_1, True))
                root.bind('<KeyRelease-Escape>', lambda event: keyPress(self.button_1, False))

        class Box_1(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Settings', padding=data['paddingSize']['labelFrame'])

                for index in range(2):
                    self.columnconfigure(index, weight=1, uniform='1')
                for index in range(5):
                    self.rowconfigure(index, weight=1, minsize=data['rowSize']['label'])

                self.add_widgets()

            def add_widgets(self):

                # Settings Labels
                self.label_1 = ttk.Label(self, text='Camera Resolution')
                self.label_2 = ttk.Label(self, text='Target FPS')
                self.label_3 = ttk.Label(self, text='Image Resolution')
                self.label_4 = ttk.Label(self, text='Image FPS')

                # LiveLabels
                self.output_1 = ttk.Label(self, text='-')
                registerLiveLabel('camResolution', self.output_1)
                self.output_2 = ttk.Label(self, text='-')
                registerLiveLabel('camFPS', self.output_2)
                self.output_3 = ttk.Label(self, text='-')
                registerLiveLabel('imageResolution', self.output_3)
                self.output_4 = ttk.Label(self, text='-')
                registerLiveLabel('imageFPS', self.output_4)

                # Layout
                self.label_1.grid(row=0, column=0, sticky='EW')
                self.label_2.grid(row=1, column=0, sticky='EW')
                self.label_3.grid(row=3, column=0, sticky='EW')
                self.label_4.grid(row=4, column=0, sticky='EW')
                self.output_1.grid(row=0, column=1, sticky='E')
                self.output_2.grid(row=1, column=1, sticky='E')
                self.output_3.grid(row=3, column=1, sticky='E')
                self.output_4.grid(row=4, column=1, sticky='E')

        class Box_2(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Frame Settings', padding=data['paddingSize']['labelFrame'])

                for index in range(2):
                    self.columnconfigure(index, weight=1, uniform='1')
                for index in range(2):
                    self.rowconfigure(index, weight=1, minsize=data['rowSize']['label'])

                self.add_widgets()

            def add_widgets(self):

                # Camera Settings Labels
                self.label_1 = ttk.Label(self, text='Resolution')
                self.label_2 = ttk.Label(self, text='FPS')

                # LiveLabels
                self.output_1 = ttk.Label(self)
                registerLiveLabel('frameResolution', self.output_1)
                self.output_2 = ttk.Label(self)
                registerLiveLabel('frameFPS', self.output_2)

                # Layout
                self.label_1.grid(row=0, column=0, sticky='EW')
                self.label_2.grid(row=1, column=0, sticky='EW')
                self.output_1.grid(row=0, column=1, sticky='E')
                self.output_2.grid(row=1, column=1, sticky='E')

        class Box_3(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Camera', padding=data['paddingSize']['labelFrame'])

                self.label = ttk.Label(self)
                self.label.pack(expand=1)

        # Set Layout UI Boxes
        self.columnconfigure(0, weight=1, uniform='1')
        self.columnconfigure(1, weight=3, uniform='1')
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)

        Menu_Bar(self).grid(row=0, columnspan=2, sticky='EW')
        Box_1(self).grid(row=1, column=0, padx=(0, 4), pady=(4, 4), sticky='NSEW')
        # Box_2(self).grid(row=2, column=0, padx=(0, 4), pady=(4, 0), sticky='NSEW')
        self.opencv = Box_3(self)
        self.opencv.grid(row=1, rowspan=2, column=1, padx=(4, 0), pady=(4, 0), sticky='NSEW')


class Tab3(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        class Menu_Bar(ttk.Frame):
            def __init__(self, parent):
                super().__init__(parent, padding=data['paddingSize']['frame'])
                
                # Toggle GUI Control Switch
                self.switch_0 = ttk.Checkbutton(self, style='Switch.TCheckbutton', variable=root.toggle_switch_0, text='GUI', command=lambda: systemGUI(root, root.toggle_switch_0))
                self.switch_0.shouldToggle = False

                # Toggle Monitor Temperature Switch
                self.toggle_switch_1 = IntVar()
                self.switch_1 = ttk.Checkbutton(self, style='Switch.TCheckbutton', variable=self.toggle_switch_1, text='Monitor', command=lambda: switchMonitor(root, self.toggle_switch_1))

                # Toggle Temperature Graph Switch
                self.toggle_switch_2 = IntVar()
                self.switch_2 = ttk.Checkbutton(self, style='Switch.TCheckbutton', variable=self.toggle_switch_2, text='Graph', command=lambda: switchGraph(self.master.graph.label, self.toggle_switch_2))

                # Quit GUI
                self.button_1 = ttk.Button(self, style='Toggle.TButton', text='❌', command=lambda: systemShutdown(root))
                self.button_1.shouldToggle = False

                # Layout
                self.switch_0.pack(padx=(0, 4), side='left')
                self.switch_1.pack(padx=(0, 4), side='left')
                self.switch_2.pack(padx=(4, 4), side='left')
                self.button_1.pack(padx=(4, 0), side='right')

                self.bindings()

            def bindings(self):
                root.bind('<KeyPress-Escape>', lambda event: keyPress(self.button_1, True))
                root.bind('<KeyRelease-Escape>', lambda event: keyPress(self.button_1, False))

        class Box_1(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Sensor', padding=data['paddingSize']['labelFrame'])

                self.columnconfigure(0, weight=0, uniform='1', minsize=36)
                self.columnconfigure(1, weight=1)
                for index in range(6):
                    self.rowconfigure(index, weight=1, minsize=data['rowSize']['label'])

                self.add_widgets()

            def add_widgets(self):
                
                # Sensor Buttons
                self.var = IntVar()
                self.radio_1 = ttk.Radiobutton(self, style='Toggle.TButton', variable=self.var, value=0, text='1', command=lambda: selectSensor(self.var))
                self.radio_2 = ttk.Radiobutton(self, style='Toggle.TButton', variable=self.var, value=1, text='2', command=lambda: selectSensor(self.var))
                self.radio_3 = ttk.Radiobutton(self, style='Toggle.TButton', variable=self.var, value=2, text='3', command=lambda: selectSensor(self.var))
                self.radio_4 = ttk.Radiobutton(self, style='Toggle.TButton', variable=self.var, value=3, text='4', command=lambda: selectSensor(self.var))
                self.radio_5 = ttk.Radiobutton(self, style='Toggle.TButton', variable=self.var, value=4, text='5', command=lambda: selectSensor(self.var))
                self.radio_6 = ttk.Radiobutton(self, style='Toggle.TButton', variable=self.var, value=5, text='6', command=lambda: selectSensor(self.var))

                # Sensor Labels
                self.label_1 = ttk.Label(self, text='Sensor 1')
                self.label_2 = ttk.Label(self, text='Sensor 2')
                self.label_3 = ttk.Label(self, text='Sensor 3')
                self.label_4 = ttk.Label(self, text='Sensor 4')
                self.label_5 = ttk.Label(self, text='Sensor 5')
                self.label_6 = ttk.Label(self, text='Sensor 6')

                # Layout
                self.radio_1.grid(row=0, column=0, pady=(0, 4), sticky='EW')
                self.radio_2.grid(row=1, column=0, pady=(4, 4), sticky='EW')
                self.radio_3.grid(row=2, column=0, pady=(4, 4), sticky='EW')
                self.radio_4.grid(row=3, column=0, pady=(4, 4), sticky='EW')
                self.radio_5.grid(row=4, column=0, pady=(4, 4), sticky='EW')
                self.radio_6.grid(row=5, column=0, pady=(4, 0), sticky='EW')

                self.label_1.grid(row=0, column=1, padx=(8, 0), pady=(0, 4), sticky='W')
                self.label_2.grid(row=1, column=1, padx=(8, 0), pady=(4, 4), sticky='W')
                self.label_3.grid(row=2, column=1, padx=(8, 0), pady=(4, 4), sticky='W')
                self.label_4.grid(row=3, column=1, padx=(8, 0), pady=(4, 4), sticky='W')
                self.label_5.grid(row=4, column=1, padx=(8, 0), pady=(4, 4), sticky='W')
                self.label_6.grid(row=5, column=1, padx=(8, 0), pady=(4, 0), sticky='W')

        class Box_2(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Monitor', padding=data['paddingSize']['labelFrame'])

                class add_widgets_top(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        for index in range(2):
                            self.columnconfigure(index, weight=1, uniform='1')
                        for index in range(4):
                            self.rowconfigure(index, weight=1, minsize=data['rowSize']['label'])

                        # Temperature
                        self.label_1 = ttk.Label(self, text='Current Temp')
                        self.label_2 = ttk.Label(self, text='Highest Temp')
                        self.label_3 = ttk.Label(self, text='Lowest Temp')

                        # LiveLabels
                        self.output_1 = ttk.Label(self, text='-')
                        registerLiveLabel('currentTemp', self.output_1)
                        self.output_2 = ttk.Label(self, text='-')
                        registerLiveLabel('highestTemp', self.output_2)
                        self.output_3 = ttk.Label(self, text='-')
                        registerLiveLabel('lowestTemp', self.output_3)

                        # Layout
                        self.label_1.grid(row=0, column=0, sticky='EW')
                        self.label_2.grid(row=2, column=0, sticky='EW')
                        self.label_3.grid(row=3, column=0, sticky='EW')
                        self.output_1.grid(row=0, column=1, sticky='E')
                        self.output_2.grid(row=2, column=1, sticky='E')
                        self.output_3.grid(row=3, column=1, sticky='E')

                class add_widgets_bot(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        # Clear Temperature Button
                        self.button_1 = ttk.Button(self, style='Toggle.TButton', text='Clear', command=lambda: clearTemp())
                        self.button_1.pack(fill='x')

                add_widgets_top(self).pack(fill='x', side='top')
                add_widgets_bot(self).pack(fill='x', side='bottom')

        class Box_3(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Graph', padding=data['paddingSize']['labelFrame'])

                self.label = ttk.Label(self)
                self.label.pack(expand=1)

        # Set Layout UI Boxes
        self.columnconfigure(0, weight=1, uniform='1')
        self.columnconfigure(1, weight=3, uniform='1')
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)

        Menu_Bar(self).grid(row=0, columnspan=2, sticky='EW')
        Box_1(self).grid(row=1, column=0, padx=(0, 4), pady=(4, 4), sticky='NSEW')
        Box_2(self).grid(row=2, column=0, padx=(0, 4), pady=(4, 0), sticky='NSEW')
        self.graph = Box_3(self)
        self.graph.grid(row=1, rowspan=2, column=1, padx=(4, 0), pady=(4, 0), sticky='NSEW')


class App(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create Notebook & Tabs as Frames
        self.notebook = ttk.Notebook(self, style='TNotebook')
        self.tab_1 = ttk.Frame(self.notebook, padding=data['paddingSize']['appFrame'])
        self.tab_2 = ttk.Frame(self.notebook, padding=data['paddingSize']['appFrame'])
        self.tab_3 = ttk.Frame(self.notebook, padding=data['paddingSize']['appFrame'])

        # Add Tabs in Notebook
        self.notebook.add(self.tab_1, text='Home')
        self.notebook.add(self.tab_2, text='Cam')
        self.notebook.add(self.tab_3, text='Graph')
        self.notebook.pack(expand=1, fill='both')

        # Layout for Each Tab Frame
        Tab1(self.tab_1).pack(expand=1, fill='both')
        Tab2(self.tab_2).pack(expand=1, fill='both')
        Tab3(self.tab_3).pack(expand=1, fill='both')

        # Initialise All Buttons to be Disabled Except Power & Close Button (shouldToggle = False)
        toggleAllChildren(self, False)


def main():
    global root
    root = tk.Tk()

    # Configure the root window
    root.title('GUI')
    w = data['windowSettings']['width']     # 1024px
    h = data['windowSettings']['height']    # 600px

    # Calculate Starting X and Y coordinates for Window
    x = (root.winfo_screenwidth()/2) - (w/2)
    y = (root.winfo_screenheight()/2) - (h/2)

    # Open window at the center of the screen and is borderless
    root.geometry('%dx%d+%d+%d'%(w, h, x, y))
    root.overrideredirect(data['windowSettings']['borderless'])
    root.resizable(width=data['windowSettings']['resizable'], height=data['windowSettings']['resizable'])

    # Set theme
    sv.set_theme('dark')
    
    # Set Default Fonts (TkDefaultFont/SunValleyBodyFont/SunValleyBodyStrongFont)
    default_font = font.nametofont('SunValleyBodyFont')
    default_font.configure(family=data['fontSettings']['family'], size=data['fontSettings']['size'])
    default_font = font.nametofont('SunValleyBodyStrongFont')
    default_font.configure(family=data['fontSettings']['family'], size=data['fontSettings']['size'])

    App(root).pack(expand=1, fill='both')

    updateLiveLabel(root)   # Initialise Registered Labels
    root.mainloop()


if __name__ == '__main__':
    print(f'GUI.py Loaded in {str(time.time() - startTime)}s')
    main()
  