from matplotlib.markers import MarkerStyle
import matplotlib.pyplot as plt
from LoadLocationData import LoadLocationData
from getLineIds import LineIds
import numpy as np
from getStopLocations import getStopLocations

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
    times = stops.keys()
    return times

def getDecimalTime(datetime):
    splitted = [char for char in str(datetime)]
    minute = int(splitted[14]+splitted[15])+float(splitted[17]+splitted[18])/60
    hour = int(splitted[11]+splitted[12])+(minute/60)+1
    return hour

def getMinute(time):
    hour = np.floor(time)
    minute = (time-hour)*60
    return minute

def getLeaveStopTime(times):
    leaveTimeList = []
    decTimeList = []
    for time in times:
        hour = getDecimalTime(time)
        decTimeList.append(hour)
    for i in range(2,len(decTimeList)-1):
        if abs(decTimeList[i] - decTimeList[i+1]) > 0.02 and abs(decTimeList[i-2] - decTimeList[i]) < 0.04:
            leaveTimeList.append(decTimeList[i])
    return leaveTimeList

def getStopLatLong(stopName, line, direction):

    stopLocations = getStopLocations()
    if direction == 'inbound':
        dir = 1
    else:
        dir = 0
    forDirection = stopLocations[line][dir]
    forStop = forDirection[forDirection['Name']==stopName]
    loc = [float(forStop['Lat'].to_list()[0]),float(forStop['Long'].to_list()[0])]
    return loc

def findLeaveTimes(filename, stopName, line, direction):
    location = getStopLatLong(stopName, line, direction)
    times = getTimeFromLocation(filename, location, line)
    leaveTimeList = getLeaveStopTime(times)
    return leaveTimeList

def plotStopTimes(leaveTimeList, stopName, line, direction):
    hours, mins = [], []
    for time in leaveTimeList:
        minute = getMinute(time)
        hours.append(time)
        mins.append(minute)
    plt.scatter(hours, mins, s=10, c='b')
    plt.xlabel('Hour of the day')
    plt.ylabel('Minute')
    plt.title('Line: '+line+', direction: '+direction+', stop: '+stopName)

def plotTimetableLines(minutes):

    for minute in minutes:
        plt.axhline(y=minute, color='r', linestyle='-')

#def findLateness(timetable):

def plotTimetable(timetable):
    hours = []
    mins = []
    for time in timetable:
        min = getMinute(time)
        hours.append(time)
        mins.append(min)
    plt.scatter(hours,mins,s=40,c='r',marker='*')  

filenames = ['LocationDataLog19-10-2021,18;16;05RunTime28800.json','LocationDataLog26-10-2021,12;20;15RunTime14400.json','LocationDataLog26-10-2021,19;38;25RunTime25200.json','LocationDataLog27-10-2021,19;26;47RunTime32400.json']
timetable = [9.2,10.45,12.71,14.12,15.65]
for file in filenames:
    leaveTimes = findLeaveTimes(file,'Filton Avenue, Lockleaze Road','73','inbound')
plotStopTimes(leaveTimes,'Filton Avenue, Lockleaze Road','73','inbound')
plotTimetable(timetable)
plt.grid()
plt.show()