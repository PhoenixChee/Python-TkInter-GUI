import numpy as np

arrayList = {}
for num in range(0, 6):
    arrayList[f'sensor{num}'] = 0, 999

print(arrayList)

for num in range(0, 6):
    highestTemp = round(np.random.uniform(0.0, 100.0), 2)
    lowestTemp = round(np.random.uniform(0.0, 100.0), 2)
    arrayList[f'sensor{num}'] = highestTemp, lowestTemp
    print(arrayList[f'sensor{num}'])

print(arrayList[f'sensor{2}'][1])
