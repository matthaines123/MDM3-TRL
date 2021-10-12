from getLocationData import getBusData
import matplotlib.pyplot as plt

#Getting the Location data from open data source
timestamp, busData = getBusData(699)

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

def getBusLocations(busData):
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


plotLatLong(getBusLocations(busData))
#getAllAttributes(busData)