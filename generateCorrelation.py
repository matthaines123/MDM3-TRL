import matplotlib.pyplot as plt
from calcPunctuality import findMeanPunct
from findLeaveTimes import leaveTimes
from importTimetable import onlyNeededTimetable
from datetime import datetime
from getTrafficData import getTrafficForRange
from LoadLocationData import listFilenames
from anprCameraRoutes import getTimesBetweenStops, getDistanceBetweenStops
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

def getTrafficSpeeds(timeRange, roadName, date):
    return getTrafficForRange(timeRange, roadName, date)

def getBusLateness(FILENAMES, stop, lines, direction, stopLocation, popTime):
    atimes, ltimes = leaveTimes(FILENAMES, stop, lines, direction, stopLocation, popTime)
    timetable = onlyNeededTimetable(direction, lines, stop)
    hours, means, medians, vars = findMeanPunct(timetable, ltimes, lines)
    return means, hours

def getBusSpeeds(ANPRFILE, filenames,  roadName, stops, lines, direction, ids, timeRange, stopLocation, popTime):
    times = getTimesBetweenStops(stops[0], stops[1], lines, ids, filenames, stopLocation, direction, timeRange, popTime)
    distance = getDistanceBetweenStops(stops[0], stops[1], lines, ids)
    busSpeeds = [float(distance)/(time*1609) for time in times]
    return busSpeeds


def createCorrelation(list1, list2, measureOne, measureTwo, stop):
    rCoeff, pval = pearsonr(list1, list2)
    print(rCoeff, pval)
    plt.scatter(list1, list2)
    plt.title('Scatter plot to show the correlation between ' + measureOne + ' and ' + measureTwo + ' at ' + stop)
    plt.xlabel(measureOne)
    plt.xlabel(measureTwo)
    plt.show()

def plotPunct(times, means, direction, stop):
    plt.bar(times, means, width=1.0, align='edge')
    #plt.scatter(times+0.5, medians, c='k')
    #plt.scatter(times+0.5, sd, c='g')
    plt.axhline(y=0, color='r', linestyle='-')
    plt.legend(['On time', 'Median', 'Standard deviation', 'Punctuality'])
    plt.title('Histogram for the mean minutes all ' + direction + ' buses leave ' + stop + ' behind schedule for the the hours in the day')
    plt.xlabel('Time of the day')
    plt.ylabel('Time behind schedule/minutes')
    plt.show()

#Defining Constants

FILENAMES = listFilenames()
#FILENAMES = ['LocationDataLog27-10-2021,19;26;47RunTime32400.json','LocationDataLog19-10-2021,18;16;05RunTime28800.json','LocationDataLog26-10-2021,12;20;15RunTime14400.json','LocationDataLog26-10-2021,19;38;25RunTime25200.json']

ANPRFILENAME = 'dim-journey-links.json'

#Defining variables
roadName = 'Anchor'
# Only put the lines in that we have files for in the RawTimetableData folder!!!
lines = ['4','3']
# inbound/southbound or outbound/northbound
direction = 'outbound'
# first stop followed by the second the bus goes though - see overleaf
busStopNames = ['College Green', 'The Centre']
stopNameFromFile = 'Bristol College Green (P1)'
# Take the longs/lats from key list.txt
stopLocation = [['51.453420', '-2.601350'],['51.454920', '-2.596850']]
# Found in the key list.txt
ids = ['0100BRP90326', '0100BRP90337']
timeRange = [8, 20]
duration = 30


busSpeed = getBusSpeeds(ANPRFILENAME, FILENAMES, roadName, busStopNames, lines, direction, ids, timeRange, stopLocation, True)
print(busSpeed)

trafficSpeed = getTrafficSpeeds(timeRange, roadName, duration)
print(trafficSpeed)

punctuality, hours = getBusLateness(FILENAMES, stopNameFromFile, lines, direction, stopLocation[0], False)
print(punctuality)

createCorrelation(busSpeed, trafficSpeed, 'bus speed', 'traffic speed', stopNameFromFile)
createCorrelation(busSpeed, punctuality, 'bus speed', 'punctuality', stopNameFromFile)
createCorrelation(trafficSpeed, punctuality, 'traffic speed', 'punctuality', stopNameFromFile)
plotPunct(hours, punctuality, direction, stopLocation[0])





