def keyPress(widget, pressed):
    # If the button is disabled don't do anything
    if widget.instate(['disabled']):
        return

    # If pressed set state to selected
    if pressed and widget.instate(['!selected']):
        widget.state(['selected'])
        widget.invoke()
    elif not pressed and widget.instate(['selected']):
        widget.state(['!selected'])


def moveAccelerate():
    print("Speed Up")


def moveDecelerate():
    print("Speed Down")


def moveSteerLeft():
    print("Steering Left")


def moveSteerRight():
    print("Steering Right")


def moveBrake():
    print("Braking...")


def calibrateODrive():
    print("Calibrating Odrive")


def calibrateM1():
    print("Calibrating M1")


def calibrateM2():
    print("Calibrating M2")


def calibrateBoth():
    print("Calibrating M1 & M2")


def calibrateSteering():
    print("Calibrating Steering")


def stopODrive():
    print("Stop Odrive")


def systemShutdown(root):
    print("System Shutting Down")
    root.destroy()


def switchPower(frame, toggle):
    if toggle.get() == 1:
        toggleAllChildren(frame, True)
        print('All Controls are ACTIVE')
    elif toggle.get() == 0:
        toggleAllChildren(frame, False)
        print('All Controls are DISABLED')


def shouldToggle(frame):
    # Check if the item should be toggled (Default is True)
    shouldToggle = True

    # shouldToggle will override all other overrides (You can put other overrides here)
    if hasattr(frame, 'shouldToggle'):
        shouldToggle = frame.shouldToggle    # True / False

    if shouldToggle:
        return True
    else:
        return False


def toggleAllChildren(frame, toggle):
    # hasattr check if the attribute is defined
    # len(frame.winfo_children()) gets the length of the list
    if not hasattr(frame, 'winfo_children') or len(frame.winfo_children()) == 0:
        # Check if the item should be toggled. If not skip this item.
        if shouldToggle(frame):  # True/False
            # Toggle the item using state attribute
            if toggle:
                frame.state(['!disabled'])  # True
            else:
                frame.state(['disabled'])   # False
    else:
        for frame in frame.winfo_children():
            # Try toggling item's children
            toggleAllChildren(frame, toggle)


def switchControlMode(toggle):
    if toggle.get() == 1:
        print("Mode: Open Loop")
    elif toggle.get() == 0:
        print("Mode: Close Loop")


def switchCamera(frame, toggle):
    if toggle.get() == 1:
        frame.is_running = True
        frame.thread = threading.Thread(target=frame.videoLoop, args=())
        frame.thread.daemon = True
        frame.thread.start()
        print("Show Camera On Display: Enabled")
    elif toggle.get() == 0:
        frame.is_running = False
        frame.after(20)
        if frame.thread is not None:
            frame.thread.join(0.2)
        frame.winfo_toplevel().destroy()
        print("Show Camera On Display: Disabled")

def videoLoop(frame, port):
    cap = cv2.VideoCapture(port)

    while frame.is_running:
        cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
        frame.queue.put(image)

def queueNextFrame(frame, eventargs):
    if not frame.queue.empty():
        image = frame.queue.get()
        image = Image.fromarray(image)
        frame.photo = ImageTk.PhotoImage(image)
        frame.view.configure(image=frame.photo)