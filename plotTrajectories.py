from LoadLocationData import LoadLocationData
from visualiseLocationData import getBusLocationsDict
from visualiseWithMaps import makeCartopyMap
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import random

def getChosenBusRoutes(dataAtTimes, busId):

    """ Reduces data to include only busId's given """

    ''' Allow a random selection of busId's by busId = the number of busId's to be selected '''
    if type(busId) is int:
        firsttime = list(dataAtTimes.keys())[0]
        keys = list(dataAtTimes[firsttime].keys())
        busId = random.choices(keys, k=busId)
    else:
        busId = busId

    chosenBusRoutesDict = {}

    for time in dataAtTimes:

        dataAtSingleTime = dataAtTimes[time]
        busLocationData = {k: dataAtSingleTime[k] for k in busId}
        chosenBusRoutesDict[time] = busLocationData

    return chosenBusRoutesDict

def reduceBusesDf(dataAtTimes, busId):

    singleBusDict = {}

    for time in dataAtTimes:

        dataAtSingleTime = dataAtTimes[time]
        for k in busId:
            singleBusDict[time] = dataAtSingleTime[k]

    return pd.DataFrame.from_dict(singleBusDict, orient='index')

def plotTrajectory(dataAtTimes, getBusLocationsDict, busId):

    ''' Plot the trajectory of a bus 
        by plotting the longitude and latitude of a bus over the location data time input '''

    locationDict = getChosenBusRoutes(dataAtTimes, busId)

    lats, longs = [], []
    for key, vals in locationDict.items():
        valdict = vals
        for key, val in valdict.items():
            lats.append(float(val[0]))
            longs.append(float(val[1]))

    plt.scatter(longs, lats, s=10, alpha=0.01)
    plt.show()

if __name__ == '__main__':
    dataAtTimes = LoadLocationData('LocationDataLog18-10-2021,16;53;01RunTime1800.json')
    busesDf = reduceBusesDf(dataAtTimes, ['69511'])
    makeCartopyMap(busesDf)
    
