import matplotlib.pyplot as plt
import numpy as np
from calcPunctuality import getMinute
from findLeaveTimes import leaveTimes

def plotStopTimes(leaveTimes, stopName, line, direction):
    hours, mins = [], []
    for time in leaveTimes:
        minute = getMinute(time)
        hours.append(time)
        mins.append(minute)
    ##### NEED TO CONVERT SOME OF THESE HOURS INTO BST #####
    plt.scatter(hours, np.zeros_like(hours) + 0, s=10, c='b')
    #plt.scatter(hours, mins, s=10, c='b')
    plt.xlabel('Hour of the day')
    plt.ylabel('Minute')
    plt.title('Line: '+line+', direction: '+direction+', stop: '+stopName)
    return hours

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

if __name__ == '__main__':
    ''' Parameters to change '''
    filenames = ['LocationDataLog27-10-2021,19;26;47RunTime32400.json','LocationDataLog19-10-2021,18;16;05RunTime28800.json','LocationDataLog26-10-2021,12;20;15RunTime14400.json','LocationDataLog26-10-2021,19;38;25RunTime25200.json']
    busStopName = 'Filton Avenue, Lockleaze Road'
    # Single bus line or all
    line = '73'
    direction = 'inbound'
    # Can either find this or put in the lat/longs
    stopLocations = 'find'
    ''' Code to call - Choose plots wanted '''
    times = leaveTimes(filenames, busStopName, line, direction, stopLocations)
    plotStopTimes(times, busStopName, line, direction)
    plotTimetable(timetable)
    plt.grid()
    plt.show()