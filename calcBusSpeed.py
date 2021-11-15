import json
import pandas as pd
from collections import defaultdict
import haversine
from haversine import haversine, Unit
import geopy
from geopy import distance
import itertools


def LoadLocationData(filename):
    ''' Loads the saved live location data, output as a dataframe '''

    if '.json' in filename:
        filename = filename
    else:
        filename = filename + '.json'

    with open('/Users/ryu/Documents/Location_Data_files/' + filename, 'r') as fp:
        dataAtTimes = json.load(fp)
        df = pd.DataFrame(data=dataAtTimes)
        return df


def getSingleLine(df, line):
    indexes = df.index
    AllLineIds = LineIds()
    IdsForLineFull = AllLineIds[line]
    IdsForLine = [x for x in IdsForLineFull if x in indexes]
    dfLine = df.loc[IdsForLine]
    return dfLine


def LineIds():
    LineRefDF = LoadFile('LineReferences26-10-2021,19;40;41RunTime25200.json')
    LineRefs = LineRefDF.iloc[:, 0]
    LineRefs = LineRefs.dropna(axis=0)
    LineRefDict = defaultdict(list)
    for i in range(len(LineRefs) - 1):
        LineRefDict[LineRefs[i][0]].append(LineRefs.index.values[i])

    return LineRefDict


def LoadFile(filename):
    ''' Loads the saved live location data, output as a dataframe '''

    if '.json' in filename:
        filename = filename
    else:
        filename = filename + '.json'

    with open('Location_Data_files/' + filename, 'r') as fp:
        dataAtTimes = json.load(fp)
        df = pd.DataFrame(data=dataAtTimes)

    return df


def getTimeFromLocation(filename, location, line):
    accuracy = 3
    locations = [location]
    truncatedStopLocations = [[round(i, accuracy) for i in stop] for stop in locations]
    df = LoadLocationData(filename)
    dfLine = getSingleLine(df, line)
    busDict = dfLine.to_dict()
    times = []
    stops = {}
    for time, bus in busDict.items():
        for busID, location in bus.items():
            if type(location) == list:
                location = [round(i, accuracy) for i in list(map(float, location))]
                if location in truncatedStopLocations:
                    stops[time] = [busID, location]
    times = stops.keys()
    print(df)
    checkCoords(df, location)
    return times


def checkCoords(df, stopLoc):
    locationData = []
    timeStamps = list(df.columns.values)
    for t in timeStamps:
        for index, column in df.iterrows():
            if isinstance(column[t], list):
                busCoords = column[t]
                if distance.distance(stopLoc, busCoords).meters <= 1:
                    locationStamp = str(index) + ', ' + str(t) + ', ' + str(busCoords)
                    locationData.append(locationStamp)
    for bus in locationData:
        print(bus)
    # print(locationData[0])
    # print(locationData[2])


def calculateSpeed(a, b, t):
    dist = haversine(a, b, unit=Unit.MILES)
    print(str(dist) + ' miles')
    time = t / 60
    speed = dist // time
    print(str(speed) + ' miles per hour')


# Apsley Road
locA = [51.468016, -2.612858]
# Clifton Down Station
locB = [51.464151, -2.609396]

# Bristol Bridge
locC = [51.45317080184595, -2.5896996088096125]
# Victoria Street
locD = [51.4508604965169, -2.586308048500305]


getTimeFromLocation('LocationDataLog27-10-2021,19;26;47RunTime32400', locA, '37613')
getTimeFromLocation('LocationDataLog27-10-2021,19;26;47RunTime32400', locB, '37613')


# calculateSpeed(locC, locD, 2)
