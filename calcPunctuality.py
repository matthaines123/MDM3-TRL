from collections import defaultdict
import numpy as np

def getMinute(time):
    hour = np.floor(time)
    minute = (time-hour)*60
    return minute

def findLateness(timetable, times):
    lateness = []
    for time in times:
        latenessForTime = [x - time for x in timetable]
        minVal = min([abs(x - time) for x in timetable])
        minute = getMinute(minVal)
        if minVal in latenessForTime:
            lateness.append(minute)
        else:
            lateness.append(-minute)
    return lateness

def findMeanPunct(timetable, times, line):
    if line == 'all' or line == 'All':
        lateness = []
        exactHours = []
        for item in list(times.keys()):
            latenessSingle = findLateness(timetable, item)
            exactHoursSingle = [np.floor(i) for i in item]
            lateness.append(latenessSingle)
            exactHours.append(exactHoursSingle)
        lateness = [item for sublist in lateness for item in sublist]
        exactHours = [item for sublist in exactHours for item in sublist]
    else:
        lateness = findLateness(timetable, times)
        exactHours = [np.floor(item) for item in times]
    eachHour = np.unique(np.array(exactHours))
    latenessDict = defaultdict(list)
    for key,value in zip(exactHours,lateness):
        latenessDict[key].append(value)
    means = []
    for key,value in latenessDict.items():
        means.append(sum(value)/len(value))
    return eachHour, means
