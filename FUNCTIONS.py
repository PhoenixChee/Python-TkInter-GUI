from GUI import *

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
    root.quit()
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
    global camOn, cam
    cam = cv2.VideoCapture(data['camSettings']['port'])

    if toggle.get() == 1:
        camOn = True
        showFrames(frame)
        print("Show Camera On Display: Enabled")
    elif toggle.get() == 0:
        camOn = False
        cam.release()
        frame.configure(image='')
        print("Show Camera On Display: Disabled")


def showFrames(frame):
    global camOn, cam
    if camOn:
        cv2image = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        frame.imgtk = imgtk
        frame.configure(image=imgtk)
        frame.after(data['camSettings']['refreshRate'], lambda: showFrames(frame))


def switchMonitor(frame, toggle):
    global monitorOn
    if toggle.get() == 1:
        monitorOn = True
        generateGraph(frame)
    elif toggle.get() == 0:
        monitorOn = False


def generateGraph(frame):
    global monitorOn
    if monitorOn:
        # Clear Plots in Graph
        plt.clf()

        # Plot & Save Graph as Transparent PNG
        plotGraph()
        plt.savefig('graph.png', transparent=True)

        # Configure Frame To Image
        photo = ImageTk.PhotoImage(file="./graph.png")
        frame.configure(image=photo)
        frame.after(data['graphSettings']['refreshRate'], lambda: generateGraph(frame))


def plotGraph():
    global x, y
    # Configure Plot Graph Colours
    ax = plt.axes()
    ax.tick_params(colors=data['graphColor']['axis'], which='both')    # Set Color to All Tick Parameters
    for spine in ax.spines.values():                                    # Set Color to All Spine
        spine.set_color(data['graphColor']['axis'])

    # Configure Plot Graph Legend
    plt.title('L to the ratio', color=data['graphColor']['font'])      # Set Color Title
    plt.xlabel('Time (s)', color=data['graphColor']['font'])           # Set Color X Label
    plt.ylabel('Temperature (°C)', color=data['graphColor']['font'])   # Set Color Y Label
    plt.ylim([1, 120])

    # Plot Graph
    plt.plot(x, y, color=data['graphColor']['line'])


def selectSensor(radio):
    global sensor
    sensor = radio.get()


def generateCoordinates():
    global arrayTemp, sensor, x, y

    # Initialise Values
    sensor = data['graphSettings']['defaultSensor']
    arrayList = {}
    for sensorNum in range(1, 7):
        arrayList['sensor{}'.format(sensorNum)] = np.array([0 for i in range(data['graphSettings']['maxPoints'])])

    while True:
        # Generate X Data (Time)
        x = np.arange(data['graphSettings']['minPoints'] - data['graphSettings']['maxPoints'], data['graphSettings']['minPoints'])

        # Generate Y Data (Temperature)
        for sensorNum in range(1, 7):
            array = arrayList['sensor{}'.format(sensorNum)]
            array = np.append(array, round(np.random.uniform(0.0, 100.0), 2))
            arrayList['sensor{}'.format(sensorNum)] = array[1:]

        # Assign Y Data Based on Selected Sensor
        for sensorNum in range(1, 7):
            if sensor == (sensorNum - 1):
                y = arrayList['sensor{}'.format(sensorNum)]
                break

        # Update Time Frame
        data['graphSettings']['minPoints'] += 1
        time.sleep(data['graphSettings']['pollingRate']/1000)


threading.Thread(target=generateCoordinates).start()


liveLabels = {}     # DataName List Registered
datas = {}          # Data List Received


def registerLiveLabel(dataName, label):
    liveLabels.update({dataName: label})


def updateLiveLabelText(frame):
    generateFakeData()

    for keyName in datas:
        if keyName in liveLabels:
            label = liveLabels.get(keyName)
            value = datas.get(keyName)
            label.config(text=value + '°C')

    frame.after(data['labelSettings']['refreshRate'], lambda: updateLiveLabelText(frame))


def generateFakeData():
    datas.update({"highestTemp": randFloatStr(0, 100.0)})
    datas.update({"lowestTemp":  randFloatStr(0, 100.0)})
    datas.update({"currentTemp": randFloatStr(0, 100.0)})


def randFloatStr(min, max):
    return str(round(np.random.uniform(min, max), 2))

