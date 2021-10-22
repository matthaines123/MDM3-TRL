from getLocationDataAtTimes import logLocationData, getBusLocationwtimes
from getLocationData import getBusData
from LoadLocationData import LoadLocationData
from visualiseLocationData import getBusLocationsDict
from visualiseWithMaps import makeCartopyMap
import matplotlib.pyplot as plt
import pandas as pd

dataAtTimes = LoadLocationData('LocationDataLog15-10-2021,12;38;16RunTime60')

def reduceNoOfBuses(dataAtTimes, busId):

    """ Reduces data to include only busId's given """

    singleBusDict = {}

    for time in dataAtTimes:

        dataAtSingleTime = dataAtTimes[time]
        busLocationData = {k: dataAtSingleTime[k] for k in busId}
        singleBusDict[time] = busLocationData

    return singleBusDict

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

    locationDict = reduceNoOfBuses(dataAtTimes, busId)

    lats, longs = [], []
    for key, vals in locationDict.items():
        valdict = vals
        for key, val in valdict.items():
            lats.append(float(val[0]))
            longs.append(float(val[1]))

    plt.scatter(longs, lats)
    plt.show()

if __name__ == '__main__':
    dataAtTimes = LoadLocationData('LocationDataLog18-10-2021,16;53;01RunTime1800.json')
    busesDf = reduceBusesDf(dataAtTimes, ['69511'])
    makeCartopyMap(busesDf)
    