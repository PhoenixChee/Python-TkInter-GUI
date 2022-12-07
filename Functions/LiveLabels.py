from GUI import *

import numpy as np


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

print('LiveLabels.py loaded')
