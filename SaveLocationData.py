from getLocationData import getBusData
from visualiseLocationData import getBusLocationsDict
from getLocationDataAtTimes import logLocationData, getBusLocationwtimes
import json
from datetime import datetime, timedelta

def SaveLocationData(getBusData, code, runTime, getBusLocationsDict, api_key):

    ''' Saves the latitude and longitude of the live location data
        for each 5 second live bus data update over a set period of time. '''

    dataAtTimes, runTime = logLocationData(getBusData, code, runTime, api_key)
    busTimeLocationDict = getBusLocationwtimes(dataAtTimes, getBusLocationsDict)
    runTime = str(runTime)
    #runTime = str(timedelta(seconds=runTime))

    '''Format of filename: Date, Time of save, length of time live data collected for'''
    filename = 'LocationDataLog' + datetime.now().strftime("%d-%m-%Y,%H;%M;%S") + 'RunTime' + runTime + '.json'
    with open('Location_Data_files/' + filename, 'w') as fp:
        json.dump(busTimeLocationDict, fp)

SaveLocationData(getBusData, 699, 12*60*60, getBusLocationsDict, api_key)