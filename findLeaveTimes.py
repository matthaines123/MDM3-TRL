from LoadLocationData import LoadLocationData
from getLineIds import LineIds
from getStopLocations import getStopLocations
from collections import defaultdict

def getSingleLine(df, line):
    indexes = df.index
    AllLineIds = LineIds()
    IdsForLineFull = AllLineIds[line]
    IdsForLine = [x for x in IdsForLineFull if x in indexes]
    dfLine = df.loc[IdsForLine]
    return dfLine

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
    times = list(stops.keys())
    return times

def getDecimalTime(datetime):
    splitted = [char for char in str(datetime)]
    minute = int(splitted[14]+splitted[15])+float(splitted[17]+splitted[18])/60
    hour = int(splitted[11]+splitted[12])+(minute/60)
    return hour

def getLeaveStopTime(times):
    leaveTimes = []
    decTimeList = []
    for time in times:
        hour = getDecimalTime(time)
        decTimeList.append(hour)
    for i in range(2,len(decTimeList)-1):
        if abs(decTimeList[i] - decTimeList[i+1]) > 0.02 and abs(decTimeList[i-2] - decTimeList[i]) < 0.04:
            leaveTimes.append(decTimeList[i])
    #leaveTimes.pop(0) # Does this need to be done?
    return leaveTimes

def getArriveStopTime(times):
    arriveTimes = []
    decTimeList = []
    for time in times:
        hour = getDecimalTime(time)
        decTimeList.append(hour)
    
    for i in range(1, len(decTimeList)):
        if abs(decTimeList[i] - decTimeList[i-1] > 0.02): #Bracket wrong here
            arriveTimes.append(decTimeList[i])
    arriveTimes.pop(-1)
    return arriveTimes    

def getStopLatLong(stopLocations, stopName, line, dir):
    forDirection = stopLocations[line][dir]
    forStop = forDirection[forDirection['Name']==stopName]
    loc = [float(forStop['Lat'].to_list()[0]),float(forStop['Long'].to_list()[0])]
    return loc

def findLeaveTimes(filename, stopLocations, stopName, line, direction):
    if len(stopLocations) == 2:
        location = [float(x) for x in stopLocations]
    else:
        location = getStopLatLong(stopLocations, stopName, line, direction)
    times = getTimeFromLocation(filename, location, line)
    arriveTimes = getArriveStopTime(times)
    leaveTimes = getLeaveStopTime(times)
    return arriveTimes, leaveTimes

def iterateThroughFiles(filenames, stopLocations, stopName, line, direction):
    ltimes = []
    atimes = []
    for file in filenames:
        arriveTimes, leaveTimes = findLeaveTimes(file, stopLocations, stopName, line, direction)
        if '-10-' in file :
            arriveTimes = [x+1 for x in arriveTimes]
            leaveTimes  = [x+1 for x in leaveTimes]
        ltimes.append(leaveTimes)
        atimes.append(arriveTimes)
    ltimes = [item for sublist in ltimes for item in sublist]
    atimes = [item for sublist in atimes for item in sublist]
    return atimes, ltimes

def leaveTimes(filenames, stopName, lines, direction, stopLocations):
    if direction == 'inbound' or direction == 'southbound' or direction == 'citybound':
        dir = 1
    else:
        dir = 0
    if stopLocations == 'find' or stopLocations == 'Find':
        stopLocations = getStopLocations()
    ltimes = defaultdict(list)
    atimes = defaultdict(list)
    for item in lines:
        arriveTimes, leaveTimes = iterateThroughFiles(filenames, stopLocations, stopName, item, dir)
        ltimes[item] = leaveTimes
        atimes[item] = arriveTimes
    return atimes, ltimes