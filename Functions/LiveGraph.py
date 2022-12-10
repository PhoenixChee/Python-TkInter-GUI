from GUI import *
from Functions.Thermostat import readTemp

from PIL import ImageTk

import numpy as np
import matplotlib.pyplot as plt

currentSensor = 0
clear = False

arrayTempList = {}
monitorTempList = {}

for n in range(6):
    arrayTempList[f'sensor{n}'] = np.zeros(60, dtype=float)
    monitorTempList[f'sensor{n}'] = np.array([0, 999])


def switchMonitor(frame, toggle):
    global monitorOn
    if toggle.get() == 1:
        monitorOn = True
        getTemp(frame)

    elif toggle.get() == 0:
        monitorOn = False


def switchGraph(frame, toggle):
    global graphOn
    if toggle.get() == 1:
        graphOn = True
        updateGraphTemp(frame)

    elif toggle.get() == 0:
        graphOn = False


def selectSensor(radio):
    global currentSensor
    currentSensor = radio.get()


def getTemp(frame):
    global currentTempList
    if monitorOn:
        currentTempList = readTemp()
        frame.after(data['dataSettings']['pollingRate'], lambda: getTemp(frame))


def monitorTemp():
    global clear, currentTempList, currentTemp, highestTemp, lowestTemp

    if monitorOn:
        if clear:
            # Clear Highest & Lowest Temperature Each Sensor
            currentTemp = currentTempList[f'sensor{currentSensor}']
            monitorTempList[f'sensor{currentSensor}'] = currentTemp, currentTemp
            clear = False
        else:
            # Get ALL Sensor Current Temperature
            # Compare & Record Highest & Lowest Temperature Each Sensor
            for n in range(6):
                currentTemp = currentTempList[f'sensor{n}']
                highestTemp, lowestTemp = monitorTempList[f'sensor{n}']

                if currentTemp > highestTemp:
                    highestTemp = currentTemp
                if currentTemp < lowestTemp:
                    lowestTemp = currentTemp

                monitorTempList[f'sensor{n}'] = np.array([highestTemp, lowestTemp])

        # Assign Selected Sensor Highest & Lowest Temperature for LiveLabel
        currentTemp = currentTempList[f'sensor{currentSensor}']
        highestTemp, lowestTemp = monitorTempList[f'sensor{currentSensor}']

        print(currentTemp, highestTemp, lowestTemp)
        return currentTemp, highestTemp, lowestTemp


def clearTemp():
    global clear
    clear = True


def getGraphTemp():
    global x, y, currentSensor

    # Generate X Coordinates (Time)
    x = np.arange(data['graphSettings']['minPoints'] - data['graphSettings']['maxPoints'],
                  data['graphSettings']['minPoints'])

    # Generate Y Coordinates (Temperature)
    try:
        for n in range(6):
            array = np.append(arrayTempList[f'sensor{n}'], currentTempList[f'sensor{n}'])
            arrayTempList[f'sensor{n}'] = array[1:]
    except:
        pass

    # Choose Selected Sensor Y Coordinates
    for n in range(6):
        if currentSensor == n:
            y = arrayTempList[f'sensor{currentSensor}']
            break

    # Update Time Frame
    data['graphSettings']['minPoints'] += 1


def plotGraphTemp():
    # Clear Plots
    plt.clf()

    # Configure Plot Graph Colours
    ax = plt.axes()
    ax.tick_params(colors=data['graphColor']['axis'], which='both')  # Set Color to All Tick Parameters
    for spine in ax.spines.values():  # Set Color to All Spine
        spine.set_color(data['graphColor']['axis'])

    # Configure Plot Graph Legend
    plt.xlabel('Time (s)', color=data['graphColor']['font'])  # Set Color X Label
    plt.ylabel('Temperature (°C)', color=data['graphColor']['font'])  # Set Color Y Label
    plt.ylim([1, 120])

    # Plot Graph & Save Graph as Transparent Image
    plt.plot(x, y, color=data['graphColor']['line'])
    plt.savefig('graph.png', transparent=True)
    plt.close()


def updateGraphTemp(frame):
    if graphOn:
        getGraphTemp()  # Get Graph Temperature
        plotGraphTemp()  # Plot Graph Coordinates

        # Configure Frame To Image
        photo = ImageTk.PhotoImage(file="./graph.png")
        frame.configure(image=photo)
        frame.after(data['graphSettings']['refreshRate'], lambda: updateGraphTemp(frame))


print('Imported LiveGraph.py')
