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

def findMeanPunct(timetable, times, lines):
    lateness = []
    exactHours = []
    for item in lines:
        latenessSingle = findLateness(timetable[item], times[item])
        exactHoursSingle = [np.floor(i) for i in times[item]]
        lateness.append(latenessSingle)
        exactHours.append(exactHoursSingle)
    lateness = [item for sublist in lateness for item in sublist]
    exactHours = [item for sublist in exactHours for item in sublist]
    eachHour = np.unique(np.array(exactHours))
    latenessDict = defaultdict(list)
    for key,value in zip(exactHours,lateness):
        latenessDict[key].append(value)
    means = []
    medians = []
    vars = []
    for key,value in latenessDict.items():
        means.append(np.mean(value))
        medians.append(np.median(value))
        vars.append(np.var(value))
    return eachHour, means, medians, vars

def getMoreBars(timetable, times, lines):
    lateness = []
    exactHours = []
    for item in lines:
        latenessSingle = findLateness(timetable[item], times[item])
        exactHoursSingle = [np.floor(i*4) for i in times[item]]
        lateness.append(latenessSingle)
        exactHours.append(exactHoursSingle)
    lateness = [item for sublist in lateness for item in sublist]
    exactHours = [item for sublist in exactHours for item in sublist]
    eachHour = np.unique(np.array(exactHours))
    latenessDict = defaultdict(list)
    for key,value in zip(exactHours,lateness):
        latenessDict[key].append(value)
    means = []
    medians = []
    for key,value in latenessDict.items():
        means.append(np.mean(value))
        medians.append(np.median(value))
    return eachHour, means, medians