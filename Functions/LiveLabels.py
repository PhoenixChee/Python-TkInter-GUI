from GUI import *

liveLabelsList = {}     # Each Registered Label and LabelName List
dataList = {}           # Each Received Data List


def registerLiveLabel(dataName, label):
    liveLabelsList.update({dataName: label})


def updateLiveLabel(frame):
    global currentTemp, highestTemp, lowestTemp

    # All data comes through here
    updateTempData()

    # Get Data and Matching Labels for Update
    for keyName in dataList:
        if keyName in liveLabelsList:
            label = liveLabelsList.get(keyName)
            value = str(dataList.get(keyName))
            label.config(text=value)

    frame.after(data['labelSettings']['refreshRate'], lambda: updateLiveLabel(frame))


def updateTempData():
    try:
        currentTemp, highestTemp, lowestTemp = monitorTemp()
    except:
        currentTemp, highestTemp, lowestTemp = '', '', ''

    # Update All Temperature Data
    dataList.update({"highestTemp": str(highestTemp) + ' °C'})
    dataList.update({"lowestTemp": str(lowestTemp) + ' °C'})
    dataList.update({"currentTemp": str(currentTemp) + ' °C'})



print('Imported LiveLabels.py')