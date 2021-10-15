from getLocationDataAtTimes import logLocationData, getBusLocationwtimes
from getLocationData import getBusData
from LoadLocationData import LoadLocationData
from visualiseLocationData import getBusLocationsDict
import matplotlib.pyplot as plt

dataAtTimes = LoadLocationData('LocationDataLog15-10-2021,12;38;16RunTime60')

def reduceNoOfBuses(dataAtTimes, busId):

    """ Reduces data to include only busId's given """

    singleBusDict = {}

    for time in dataAtTimes:

        dataAtSingleTime = dataAtTimes[time]
        busLocationData = {k: dataAtSingleTime[k] for k in busId}
        singleBusDict[time] = busLocationData

    return singleBusDict

def plotTrajectory(dataAtTimes, getBusLocationsDict, busId):

    ''' Plot the trajectory of a bus 
        by plotting the longitude and latitude of a bus over the location data time input '''

    locationDict = reduceNoOfBuses(dataAtTimes, getBusLocationsDict, busId)

    lats, longs = [], []
    for key, vals in locationDict.items():
        valdict = vals
        for key, val in valdict.items():
            lats.append(float(val[0]))
            longs.append(float(val[1]))

    plt.scatter(longs, lats)
    plt.show()
        
plotTrajectory(dataAtTimes, getBusLocationsDict, ['69511'])