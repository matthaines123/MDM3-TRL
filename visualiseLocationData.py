from getLocationData import getBusData
import matplotlib.pyplot as plt
import math
from collections import ChainMap
import pandas as pd
import numpy as np


#Getting the Location data from open data source
routeIDs = []
routeID = 2093

def getAllAttributes(busData):
    '''
    Function used to print all attributes associated with each of the buses
    '''
    def recursiveDict(busData):
        for key, val in busData.items():
            if type(val) is dict:
                yield from recursiveDict(val)
            else:
                yield (key, val)

    for key, value in recursiveDict(busData[0]):
        print(key, value,'\n')

def getBusLocationsDict(busData):
    '''
    Returns a dict of bus latitudes and longitudes, the keys for the dictionary
    are the bus vehicle references
    '''
    busLocationDict = {}
    #Iterates over each bus in the dataset
    for bus in busData:
        singleBusData = bus['MonitoredVehicleJourney']
        #Gets position
        busLatLong = [singleBusData['VehicleLocation']['Latitude'], singleBusData['VehicleLocation']['Longitude']]
        #Get busId
        busID = singleBusData['VehicleRef']
        busLocationDict[busID] = busLatLong
    return busLocationDict

def getBusLocationsDF(busLocationDict):
    '''
    Returns a pandas dataframe of the data in the bus location dictionary
    '''
    df = pd.DataFrame(data = busLocationDict)
    return df.transpose()

            
def allIDs(routeIDs):
    '''
    Function that can be used to get the coords of buses
    across lot's of operators
    '''
    allData = []
    if routeIDs == []:
        routeIDs = range(0, 10000)
    #Iterating over each operator
    for i in routeIDs:
        timestamp, data = getBusData(i)
        if data != False:
            busData = getBusLocationsDict(data)
            allData.append(busData)
    #Convert list of dicts to one dict
    busData = dict(ChainMap(*allData))
    plotLatLong(busData)


def singleId(routeID):
    '''
    Plotting the gps of buses from a single operator
    '''
    timestamp, busData = getBusData(routeID)
    plotLatLong(getBusLocationsDict(busData))


            
def plotLatLong(busLocationDict):
    '''
    Plotting the buses on a matplotlib scatter plot
    '''
    lats, longs = [], []
    for key, vals in busLocationDict.items():
        lats.append(float(vals[0]))
        longs.append(float(vals[1]))

    plt.scatter(longs, lats)
    plt.show()

#allIDs(routeIDs)
#getAllAttributes(busData)