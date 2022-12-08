from GUI import *

liveLabelsList = {}     # Each Registered Label and LabelName List
dataList = {}           # Each Received Data List

tempList = {}           # Each Sensor Highest & Lowest Temperature List
for n in range(0, 6):
    tempList[f'sensor{n}'] = (0, 999)

clear = False


def registerLiveLabel(dataName, label):
    liveLabelsList.update({dataName: label})


def updateLiveLabel(frame):
    getTempData()
    updateData()

    # Get Data and Matching Labels for Update
    for keyName in dataList:
        if keyName in liveLabelsList:
            label = liveLabelsList.get(keyName)
            value = str(dataList.get(keyName))
            label.config(text=value + ' °C')

    frame.after(data['labelSettings']['refreshRate'], lambda: updateLiveLabel(frame))


def clearTemp():
    global clear
    clear = True


def getTempData():
    global highestTemp, lowestTemp, currentTemp, currentTempList, currentSensor, clear

    # Get Current Temperature & Sensor
    while not queue.empty():
        currentTempList, currentSensor = queue.get()

    # Check if Clear Button is Pressed
    if clear:
        currentTemp = currentTempList[f'sensor{currentSensor}']
        tempList[f'sensor{currentSensor}'] = currentTemp, currentTemp
        clear = False
    else:
        for n in range(0, 6):
            # Get All Temperature
            currentTemp = currentTempList[f'sensor{n}']
            highestTemp, lowestTemp = tempList[f'sensor{n}']

            # Compare Highest & Lowest Temperature with Current Temperature
            if currentTemp > highestTemp:
                highestTemp = currentTemp
            if currentTemp < lowestTemp:
                lowestTemp = currentTemp

            # Record Highest & Lowest Temperature for Each Sensor
            tempList[f'sensor{n}'] = highestTemp, lowestTemp

    # Highest & Lowest Temperature for Selected Sensor
    currentTemp = currentTempList[f'sensor{currentSensor}']
    highestTemp, lowestTemp = tempList[f'sensor{currentSensor}']


def updateData():
    # Update All Temperature Data
    dataList.update({"highestTemp": highestTemp})
    dataList.update({"lowestTemp": lowestTemp})
    dataList.update({"currentTemp": currentTemp})


print('Imported LiveLabels.py')
