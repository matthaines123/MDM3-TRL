from getLocationData import getBusData
from visualiseLocationData import getBusLocationsDict
import time

def logLocationData(getBusData, code, runTime):

    ''' For a given length of time to repeatadly get the live location data
        stored in a dictionary with each time as the key '''

    '''Dictionary to store the busData for each timestamp'''
    dataAtTimes = {}

    runTime = runTime # in seconds
    Timer = 0
    startTimer = time.time()

    while Timer < runTime:
        timestamp, busData = getBusData(code)
        dataAtTimes[timestamp] = busData
        Timer = time.time() - startTimer

    return dataAtTimes, runTime

def getBusLocationwtimes(dataAtTimes, getBusLocationsDict):

    ''' Simplify the data to only the latitude and longitude for each vehicle at each time. '''

    busTimeLocationDict = {}

    for time in dataAtTimes:

        dataAtSingleTime = dataAtTimes[time]

        busLocationData = getBusLocationsDict(dataAtSingleTime)

        busTimeLocationDict[time] = busLocationData

    return busTimeLocationDict