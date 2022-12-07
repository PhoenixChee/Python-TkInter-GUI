from GUI import *

liveLabels = {}

def registerLiveLabel(dataName, label):
    liveLabels.update({dataName: label})

datas = {}

def randFloatStr(min, max):
    return str(round(np.random.uniform(min, max), 2))

def generateFakeData():
    datas.update({"highestTemp": randFloatStr(0, 100.0)})
    datas.update({"lowestTemp":  randFloatStr(0, 100.0)})
    datas.update({"currentTemp": randFloatStr(0, 100.0)})

def updateLiveLabelText(frame):
    generateFakeData()

    for keyName in datas:
        if keyName in liveLabels:
            label = liveLabels.get(keyName)
            value = datas.get(keyName)
            label.config(text=value + '°C')

    frame.after(1000, lambda: updateLiveLabelText(frame))