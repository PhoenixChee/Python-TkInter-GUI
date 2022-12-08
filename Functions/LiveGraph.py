from GUI import *
from PIL import Image, ImageTk

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

queue = Queue()


def switchGraph(frame, toggle):
    global graphOn
    if toggle.get() == 1:
        graphOn = True
        generateGraph(frame)
    elif toggle.get() == 0:
        graphOn = False


def switchMonitor(toggle):
    global monitorOn
    if toggle.get() == 1:
        monitorOn = True
        print('Monitoring Temperature Values: Enabled')
    elif toggle.get() == 0:
        monitorOn = False
        print('Monitoring Temperature Values : Disabled')


def selectSensor(radio):
    global sensor
    sensor = radio.get()


def generateGraph(frame):
    global graphOn
    if graphOn:
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
    # Configure Plot Graph Colours
    ax = plt.axes()
    ax.tick_params(colors=data['graphColor']['axis'], which='both')    # Set Color to All Tick Parameters
    for spine in ax.spines.values():                                   # Set Color to All Spine
        spine.set_color(data['graphColor']['axis'])

    # Configure Plot Graph Legend
    plt.title('L to the ratio', color=data['graphColor']['font'])      # Set Color Title
    plt.xlabel('Time (s)', color=data['graphColor']['font'])           # Set Color X Label
    plt.ylabel('Temperature (°C)', color=data['graphColor']['font'])   # Set Color Y Label
    plt.ylim([1, 120])

    # Plot Graph
    plt.plot(x, y, color=data['graphColor']['line'])


# Always Generates Data, Must Loop when Program Starts
def generateFakeCoordinates():
    global x, y, sensor

    # Default Sensor Selected
    sensor = 0

    # Set List of Temperature Arrays of Each Sensor to 0
    arrayList = {}
    currentTempList = {}
    for n in range(0, 6):
        arrayList[f'sensor{n}'] = np.array([0 for i in range(data['graphSettings']['maxPoints'])])

    while True:
        # Generate X Data (Time)
        x = np.arange(data['graphSettings']['minPoints'] - data['graphSettings']['maxPoints'], data['graphSettings']['minPoints'])

        # Generate Y Data (Temperature)
        for n in range(0, 6):
            array = arrayList[f'sensor{n}']
            array = np.append(array, round(np.random.uniform(0.0, 100.0), 2))
            arrayList[f'sensor{n}'] = array[1:]

        # Assign Y Data Based on Selected Sensor
        for n in range(0, 6):
            if sensor == (n):
                y = arrayList[f'sensor{n}']
                break

        # Get List of Each Sensor Current Temperature
        for n in range(0, 6):
            currentTempList[f'sensor{n}'] = arrayList[f'sensor{n}'][-1]

        # Queue Current Temperature List for LiveLabels
        queue.put((currentTempList, sensor))

        # Update Time Frame
        data['graphSettings']['minPoints'] += 1
        time.sleep(data['graphSettings']['pollingRate']/1000)


print('Imported LiveGraph.py')
