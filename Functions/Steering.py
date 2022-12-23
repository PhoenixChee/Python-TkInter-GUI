import numpy as np

steerAngleMin = -15.0
steerAngleMax = 15.0

speedMin = -5.0
speedMax = 5.0

steerAngleDict = {}
speedDict = {}


def readSteerAngle():
    dict = steerAngleDict
    dict['currentSteerAngle'] = round(np.random.uniform(steerAngleMin, steerAngleMax), 2)
    dict['percentageSteerAngle'] = 50 + round(convert2Percentage(steerAngleMin, steerAngleMax, dict['currentSteerAngle']), 2)
    
    return dict
    
    
def readSpeed():
    dict = speedDict
    dict['currentSpeed'] = round(np.random.uniform(speedMin, speedMax), 2)
    dict['percentageSpeed'] = 50 + round(convert2Percentage(speedMin, speedMax, dict['currentSpeed']), 2)
    
    return dict


def convert2Percentage(min, max, input):
    percentageValue = (input/(max-min))*100
    
    return percentageValue