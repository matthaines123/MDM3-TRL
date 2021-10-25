from LoadLocationData import LoadLocationData
from visualiseWithMaps import makeCartopyMap
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np

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

    chosenBusRoutesDF = pd.DataFrame(data = chosenBusRoutesDict)

    return chosenBusRoutesDF, chosenBusRoutesDict

def reduceBusesDf(dataAtTimes, busId):

    if type(busId) is int:
        firsttime = list(dataAtTimes.keys())[0]
        keys = list(dataAtTimes[firsttime].keys())
        busId = random.choices(keys, k=busId)
    else:
        busId = busId

    singleBusDict = {}

    for time in dataAtTimes:

        dataAtSingleTime = dataAtTimes[time]
        for k in busId:
            singleBusDict[time] = dataAtSingleTime[k]

    return pd.DataFrame.from_dict(singleBusDict, orient='index')

def plotTrajectory(dataAtTimes, busId):

    ''' Plot the trajectory of a bus 
        by plotting the longitude and latitude of a bus over the location data time input '''

    locationDF, locationDict = getChosenBusRoutes(dataAtTimes, busId)
    """
    lats, longs = [], []
    for key, vals in locationDict.items():
        #print(vals)
        valdict = vals
        for key, val in valdict.items():
            #print(key)
            lats.append(float(val[0]))
            longs.append(float(val[1]))
            plt.scatter(longs, lats, s=10, alpha=0.05, c=np.random.rand(3))
    """
    for Id, loc in locationDF.iterrows():
        lats, longs = [], []
        #print(loc)
        for latlong in loc:
            #print(latlong)
            lats.append(latlong[0])
            longs.append(latlong[1])
        #print(lats)
        plt.scatter(longs, lats, s=10, alpha=0.05, c=np.random.rand(3))
    
    plt.show()

if __name__ == '__main__':
    dataAtTimes = LoadLocationData('LocationDataLog19-10-2021,18;16;05RunTime28800.json')
    busesDf = reduceBusesDf(dataAtTimes, 1)
    makeCartopyMap(busesDf)
    
