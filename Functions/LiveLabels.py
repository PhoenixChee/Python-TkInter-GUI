from GUI import data
from Functions.ODrive import *
from Functions.Steering import *
from Functions.LiveCam import camSettings, imageSettings
from Functions.LiveGraph import monitorTemp

liveLabelsList = {}     # Each Registered Label and LabelName List
liveBarsList = {}       # Each Registered Bar and BarName List
dataList = {}           # Each Received Data List


def registerLiveLabel(dataName, label):
    liveLabelsList.update({dataName: label})


def registerLiveBar(dataName, bar):
    liveBarsList.update({dataName: bar})


def updateLiveLabel(frame):
    # All Data Comes Through Here
    updateDashboardData()
    updateControlData()
    updateCamData()
    updateTempData()

    # Get Data and Matching Labels for Update
    for keyName in dataList:
        # Configure Label Text
        if keyName in liveLabelsList:
            label = liveLabelsList.get(keyName)
            value = dataList.get(keyName)
            label.config(text=value)
        
        # Configure Bar Value
        if keyName in liveBarsList:
            bar = liveBarsList.get(keyName)
            value = dataList.get(keyName)
            bar.config(value=value)
            
    frame.after(data['labelSettings']['refreshRate'], lambda: updateLiveLabel(frame))


def updateDashboardData():
    from Functions.LiveDashboard import monitorOn
    
    if monitorOn:
        # Update ODrive Data
        currentData = readODrive()
        dataList.update({'batteryVoltage': str(currentData.get('voltageOD')) + ' V'})
        dataList.update({'batteryTemp': str(currentData.get('tempOD')) + ' °C'})
        dataList.update({'batteryTempBar': currentData.get('tempOD')})


def updateControlData():
    from Functions.LiveDashboard import controlCloseLoop
    
    if controlCloseLoop:
        # Update Speed Data
        currentSpeed = readSpeed()
        dataList.update({'speed': str(currentSpeed.get('currentSpeed')) + ' Turns/s'})
        dataList.update({'speedBar': currentSpeed.get('percentageSpeed')})
        
        # Update Steering Data
        currentAngle = readSteerAngle()
        dataList.update({'steerAngle': str(currentAngle.get('currentSteerAngle')) + ' °'})
        dataList.update({'steerAngleBar': currentAngle.get('percentageSteerAngle')})


def updateCamData():
    from Functions.LiveCam import camOn
    
    if camOn:
        # Update Camera Settings Data
        currentCamSettings = camSettings()
        dataList.update({'camResolution': str(currentCamSettings.get('widthResolution')) + '×' + str(currentCamSettings.get('heightResolution'))})
        dataList.update({'camFPS': str(currentCamSettings.get('targetFPS')) + ' FPS'})
        
        # Update Image Settings Data
        currentImageSettings = imageSettings()
        dataList.update({'imageResolution': str(currentImageSettings.get('imageWidth')) + '×' + str(currentImageSettings.get('imageHeight'))})
        dataList.update({'imageFPS': str(currentImageSettings.get('imageFPS')) + ' FPS'})


def updateTempData():
    from Functions.LiveGraph import monitorOn

    if monitorOn:
        # Update All Temperature Data
        currentSensorTemp = monitorTemp()
        dataList.update({'currentTemp': str(currentSensorTemp.get('current')) + ' °C'})
        dataList.update({'highestTemp': str(currentSensorTemp.get('highest')) + ' °C'})
        dataList.update({'lowestTemp': str(currentSensorTemp.get('lowest')) + ' °C'})


print('Imported LiveLabels.py')