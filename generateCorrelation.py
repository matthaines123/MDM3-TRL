import pandas as pd

import LoadLocationData
import matplotlib.pyplot as plt
from calcPunctuality import findLateness, findMeanPunct, getMoreBars
from findLeaveTimes import leaveTimes
from importTimetable import onlyNeededTimetable
from datetime import datetime
from getTrafficData import getTrafficForRange
from anprCameraRoutes import getTimesBetweenStops, getDistanceBetweenStops

from scipy.stats import pearsonr
import matplotlib.pyplot as plt

def getTrafficSpeeds(timeRange, roadName, date):
    return getTrafficForRange(timeRange, roadName, date)

def getBusLateness(FILENAMES, stop, lines, direction, stopLocation):
    times = leaveTimes(FILENAMES, stop, lines, direction, stopLocation)
    timetable = onlyNeededTimetable(direction, lines, stop)
    hours, means, medians, vars = findMeanPunct(timetable, times, lines)
    return means

def getBusSpeeds(ANPRFILE, filenames,  roadName, stops, lines, direction, ids, timeRange, stopLocation):
    times = getTimesBetweenStops(stops[0], stops[1], lines, ids, filenames, stopLocation, direction, timeRange)
    distance = getDistanceBetweenStops(stops[0], stops[1], lines, ids)
    busSpeeds = [float(distance)/(time*1609) for time in times]
    return busSpeeds


#Defining Constants

FILENAMES = ['LocationDataLog27-10-2021,19;26;47RunTime32400.json','LocationDataLog19-10-2021,18;16;05RunTime28800.json','LocationDataLog26-10-2021,12;20;15RunTime14400.json','LocationDataLog26-10-2021,19;38;25RunTime25200.json']
ANPRFILENAME = 'dim-journey-links.json'

#Defining variables
roadName = 'Anchor'
lines = ['4','3']
direction = 'outbound'
busStopNames = ['College Green', 'The Centre']
stopNameFromFile = 'Bristol College Green (P1)'
stopLocation = [['51.453420', '-2.601350'],['51.454920', '-2.596850']]
ids = ['0100BRP90326', '0100BRP90337']
timeRange = [8, 20]
date = datetime(2021, 10, 19, timeRange[0])

busSpeed = getBusSpeeds(ANPRFILENAME, FILENAMES, roadName, busStopName, lines, direction, ids, timeRange, stopLocation)
trafficSpeed = getTrafficSpeeds(timeRange, roadName, date)
punctuality = getBusLateness(FILENAMES, busStopName[0], lines, direction, stopLocation[0])

print(busSpeed)
print(trafficSpeed)
print(punctuality)



rCoeff = pearsonr(speeds, means)

plt.scatter(speeds, means)
plt.show()

