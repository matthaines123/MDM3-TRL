from matplotlib.markers import MarkerStyle
import matplotlib.pyplot as plt
from numpy.lib.function_base import append
from LoadLocationData import LoadLocationData
from getLineIds import LineIds
import numpy as np
from getStopLocations import getStopLocations
from datetime import datetime

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

def roundToHour(time):
    return time.replace(microsecond=0, second=0, minute=0)

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

def getStopLatLong(stopLocations, stopName, line, direction):
    if direction == 'inbound':
        dir = 1
    else:
        dir = 0
    forDirection = stopLocations[line][dir]
    forStop = forDirection[forDirection['Name']==stopName]
    loc = [float(forStop['Lat'].to_list()[0]),float(forStop['Long'].to_list()[0])]
    return loc

def findLeaveTimes(filename, stopLocations, stopName, line, direction):
    location = getStopLatLong(stopLocations, stopName, line, direction)
    times = getTimeFromLocation(filename, location, line)
    leaveTimeList = getLeaveStopTime(times)
    return leaveTimeList

def plotStopTimes(leaveTimeList, stopName, line, direction):
    hours, mins = [], []
    for time in leaveTimeList:
        minute = getMinute(time)
        hours.append(time)
        mins.append(minute)
    hours = [item for sublist in hours for item in sublist]
    mins = [item for sublist in mins for item in sublist]
    plt.scatter(hours, np.zeros_like(hours) + 0, s=10, c='b')
    #plt.scatter(hours, mins, s=10, c='b')
    plt.xlabel('Hour of the day')
    plt.ylabel('Minute')
    plt.title('Line: '+line+', direction: '+direction+', stop: '+stopName)
    return hours

def plotTimetableLines(minutes):
    for minute in minutes:
        plt.axhline(y=minute, color='r', linestyle='-')

def findLateness(timetable, hours):
    lateness = []
    for time in hours:
        latenessForTime = [x - time for x in timetable]
        minVal = min([abs(x - time) for x in timetable])
        minute = getMinute(minVal)
        if minVal in latenessForTime:
            lateness.append(minute)
        else:
            lateness.append(-minute)
    return lateness

def plotLatenessHist(timetable, hours):
    lateness = findLateness(timetable, hours)
    plt.bar(hours, lateness, edgecolor='w')
    plt.axhline(y=0, color='r', linestyle='-')
    plt.legend(['On time','Punctuality'])
    plt.xlabel('Time of the day')
    plt.ylabel('Time behind schedule')
    plt.show()

#def differenceEqnForLateness():

def plotTimetable(timetable):
    hours = []
    mins = []
    for time in timetable:
        min = getMinute(time)
        hours.append(time)
        mins.append(min)
    plt.scatter(hours,np.zeros_like(hours) + 0,s=40,c='k',marker='*')
    #plt.scatter(hours,mins,s=40,c='k',marker='x')
    plt.legend('Estimated arrival times')

def produceTimetable():
    timetable = []
    for i in range(45):
        timetable.append(7.96 + 0.25*i)
    return timetable

if __name__ == '__main__':
    filenames = ['LocationDataLog27-10-2021,19;26;47RunTime32400.json','LocationDataLog19-10-2021,18;16;05RunTime28800.json','LocationDataLog26-10-2021,12;20;15RunTime14400.json','LocationDataLog26-10-2021,19;38;25RunTime25200.json']
    leaveTimes = []

    stopLocations = getStopLocations()
    for file in filenames:
        leaveTimesFile = findLeaveTimes(file, stopLocations, 'Filton Avenue, Lockleaze Road', '73','inbound')
        leaveTimes.append(leaveTimesFile)
    hours = plotStopTimes(leaveTimes, 'Filton Avenue, Lockleaze Road', '73', 'inbound')
    timetable = produceTimetable()
    plotTimetable(timetable)
    plt.grid()
    plt.show()
    plotLatenessHist(timetable, hours)