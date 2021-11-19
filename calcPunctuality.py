from collections import defaultdict
import numpy as np

def getMinute(time):
    hour = np.floor(time)
    minute = (time-hour)*60
    return minute

def findLateness(timetable, times):
    lateness = []
    for time in times:
        """ FOR ONLY LATE
        latenessForTime = [time - x for x in timetable]
        minVal = min([x for x in latenessForTime if x > 0])
        minute = getMinute(minVal)
        lateness.append(minute)
        """
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
    eachHour = list(np.unique(np.array(exactHours)))
    latenessDict = defaultdict(list)
    for key,value in zip(exactHours,lateness):
        latenessDict[key].append(value)
    means = []
    medians = []
    sd = []
    for key,value in latenessDict.items():
        means.append(np.mean(value))
        medians.append(np.median(value))
        sd.append(np.std(value))
    #eachHour.pop(-1)
    #means.pop(-1)
    medians.pop(-1)
    return eachHour, means, medians, sd

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
    eachHour.pop[-1]
    means.pop(-1)
    medians.pop(-1)
    return eachHour, means, medians
