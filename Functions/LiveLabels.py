from GUI import *

liveLabelsList = {}     # Each Registered Label and LabelName List
dataList = {}           # Each Received Data List


def registerLiveLabel(dataName, label):
    liveLabelsList.update({dataName: label})


def updateLiveLabel(frame):
    # All Data Comes Through Here
    updateCamData()
    updateImageData()
    updateTempData()

    # Get Data and Matching Labels for Update
    for keyName in dataList:
        if keyName in liveLabelsList:
            label = liveLabelsList.get(keyName)
            value = str(dataList.get(keyName))
            label.config(text=value)

    frame.after(data['labelSettings']['refreshRate'], lambda: updateLiveLabel(frame))


def updateCamData():
    try:
        widthResolution, heightResolution, targetFPS = camSettings()
    except:
        widthResolution, heightResolution, targetFPS = '', '', ''

    # Update Camera Settings Data
    dataList.update({'camResolution': str(widthResolution) + '×' + str(heightResolution)})
    dataList.update({'camFPS': str(targetFPS) + ' FPS'})


def updateImageData():
    try:
        imageWidth, imageHeight, imageFPS = imageSettings()
    except:
        imageWidth, imageHeight, imageFPS = '', '', ''

    # Update Image Settings Data
    dataList.update({'imageResolution': str(imageWidth) + '×' + str(imageHeight)})
    dataList.update({'imageFPS': str(imageFPS) + ' FPS'})


def updateTempData():
    try:
        currentTemp, highestTemp, lowestTemp = monitorTemp()
    except:
        currentTemp, highestTemp, lowestTemp = '', '', ''

    # Update All Temperature Data
    dataList.update({'highestTemp': str(highestTemp) + ' °C'})
    dataList.update({'lowestTemp': str(lowestTemp) + ' °C'})
    dataList.update({'currentTemp': str(currentTemp) + ' °C'})



print('Imported LiveLabels.py')