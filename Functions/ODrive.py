import numpy as np

currentODriveDict = {}

oDriveInfolist = ['voltage', 'controlLoop', 'temp']
motorInfoList = ['state', 'speed', 'current', 'calibrate', 'error', 'watchdogTimer']

    
def readODrive():
    dict = currentODriveDict
    
    ID = 'OD'
    dict[f'{oDriveInfolist[0]}{ID}'] = round(np.random.uniform(0.0, 20.0), 2)
    dict[f'{oDriveInfolist[1]}{ID}'] = True
    dict[f'{oDriveInfolist[2]}{ID}'] = round(np.random.uniform(50.0, 80.0), 2)

    ID = 'M0'
    dict[f'{motorInfoList[0]}{ID}'] = True
    dict[f'{motorInfoList[1]}{ID}'] = round(np.random.uniform(0.0, 20.0), 2)
    dict[f'{motorInfoList[2]}{ID}'] = round(np.random.uniform(11.5, 13.5), 2)
    dict[f'{motorInfoList[3]}{ID}'] = True
    dict[f'{motorInfoList[4]}{ID}'] = True
    dict[f'{motorInfoList[5]}{ID}'] = True
    
    ID = 'M1'
    dict[f'{motorInfoList[0]}{ID}'] = True
    dict[f'{motorInfoList[1]}{ID}'] = round(np.random.uniform(0.0, 20.0), 2)
    dict[f'{motorInfoList[2]}{ID}'] = round(np.random.uniform(11.5, 13.5), 2)
    dict[f'{motorInfoList[3]}{ID}'] = True
    dict[f'{motorInfoList[4]}{ID}'] = True
    dict[f'{motorInfoList[5]}{ID}'] = True
    
    return dict