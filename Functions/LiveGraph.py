from GUI import *
from Functions.Thermostat import readTemp

from PIL import ImageTk

import numpy as np
import matplotlib.pyplot as plt


# Initialise
monitorOn = False
graphOn = False

currentSensor = 0
clear = False

arrayTempList = {}
monitorTempList = {}

for n in range(6):
    arrayTempList[f'sensor{n}'] = np.zeros(data['graphSettings']['maxPoints'], dtype=float)
    monitorTempList[f'sensor{n}'] = np.array([0.0, 999.0])


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
            # Set current temperature as highest & lowest temperature for currently selected sensor
            currentTemp = currentTempList[f'sensor{currentSensor}']
            monitorTempList[f'sensor{currentSensor}'] = currentTemp, currentTemp
            clear = False
        else:
            # Get each sensor current temperature & compare their highest (default = 0) & lowest temperature (default = 999)
            for n in range(6):
                currentTemp = currentTempList[f'sensor{n}']
                highestTemp, lowestTemp = monitorTempList[f'sensor{n}']

                if currentTemp > highestTemp:
                    highestTemp = currentTemp
                if currentTemp < lowestTemp:
                    lowestTemp = currentTemp

                # Update each sensor highest & lowest temperature
                monitorTempList[f'sensor{n}'] = np.array([highestTemp, lowestTemp])

        # Get currently selected sensor highest & lowest temperature for LiveLabel
        currentTemp = currentTempList[f'sensor{currentSensor}']
        highestTemp, lowestTemp = monitorTempList[f'sensor{currentSensor}']

        return currentTemp, highestTemp, lowestTemp


def clearTemp():
    global clear
    clear = True


def getGraphTemp():
    global x, y, currentSensor

    # Generate X Coordinates (Time Array)
    x = np.arange(data['graphSettings']['minPoints'] - data['graphSettings']['maxPoints'], data['graphSettings']['minPoints'])

    # Generate Y Coordinates (Temperature Array)
    if monitorOn:
        for n in range(6):
            array = np.append(arrayTempList[f'sensor{n}'], currentTempList[f'sensor{n}'])
            arrayTempList[f'sensor{n}'] = array[1:]

    # Choose Selected Sensor as the Y Coordinates
    y = arrayTempList[f'sensor{currentSensor}']

    # Update Time Array
    data['graphSettings']['minPoints'] += 1


def plotGraphTemp():
    # Clear Plots
    plt.clf()

    # Configure Plot Graph Colours
    ax = plt.axes()
    ax.tick_params(colors=data['graphSettings']['axisColor'], which='both')     # Set Color to All Tick Parameters
    for spine in ax.spines.values():
        spine.set_color(data['graphSettings']['axisColor'])                     # Set Color to All Spine

    # Configure Plot Graph Legend
    plt.xlabel('Time (s)', color=data['graphSettings']['fontColor'])            # Set Color X Label
    plt.ylabel('Temperature (°C)', color=data['graphSettings']['fontColor'])    # Set Color Y Label
    plt.ylim([0, 120])                                                          # Set Graph Y Limits

    # Plot Graph & Save Graph as Transparent Image
    plt.plot(x, y, color=data['graphSettings']['lineColor'])
    plt.savefig('graph.png', transparent=True)
    plt.close()


def updateGraphTemp(frame):
    if graphOn:
        getGraphTemp()      # Get Graph Temperature
        plotGraphTemp()     # Plot Graph Coordinates

        # Configure Target Frame as Graph Image
        photo = ImageTk.PhotoImage(file='./graph.png')
        frame.configure(image=photo)
        frame.after(data['graphSettings']['refreshRate'], lambda: updateGraphTemp(frame))


print('Imported LiveGraph.py')
