from GUI import *
from PIL import Image, ImageTk

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


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

print('LiveGraph.py loaded')
