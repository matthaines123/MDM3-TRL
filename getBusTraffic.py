from LoadLocationData import LoadLocationData
from getTrafficData import getTrafficGates
import numpy as np


def checkGate(trafficData, busData):
    accuracy = 5
    #Accuracy 4 = 10m, accuracy 5  = 1m
    truncatedTraffic = [[round(i, accuracy) for i in location] for location in trafficData]
    #truncatedBus = [[round(float(i), accuracy) for i in location] for location in busData.to_numpy().flatten()]
    truncatedBus = []
    for location in busData.to_numpy().flatten():
        newPair = []
        if type(location) != float: 
            for i in location:
                roundedValue = round(float(i), accuracy)
                newPair.append(roundedValue)
            truncatedBus.append(newPair)
            
    for gate in truncatedTraffic:
        if gate in truncatedBus:
            print(gate)


if __name__ == '__main__':
    filename = 'LocationDataLog19-10-2021,18;16;05RunTime28800.json'
    historicData = LoadLocationData(filename)
    trafficData = getTrafficGates()
    checkGate(trafficData, historicData)