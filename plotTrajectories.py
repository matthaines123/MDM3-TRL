from LoadLocationData import LoadLocationData
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

    chosenBusRoutesDict

    return chosenBusRoutesDict
    
def plotTrajectory(dataAtTimes, busId):

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

#dfdataAtTimes, dataLines, dataAtTimes = LoadLocationData('LocationDataLog19-10-2021,18;16;05RunTime28800.json','LineReferences20-10-2021,20;58;28RunTime60.json')
dfdataAtTimes = LoadLocationData('LocationDataLog19-10-2021,18;16;05RunTime28800.json')
plotTrajectory(dfdataAtTimes, 4)