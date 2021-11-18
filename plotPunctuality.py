import matplotlib.pyplot as plt
from LoadLocationData import listFilenames
from calcPunctuality import findLateness, findMeanPunct, getMoreBars
from findLeaveTimes import leaveTimes
from importTimetable import onlyNeededTimetable

def plotLatenessHist(timetable, hours):
    lateness = findLateness(timetable, hours)
    plt.bar(hours, lateness, edgecolor='w')
    plt.axhline(y=0, color='r', linestyle='-')
    plt.legend(['On time','Punctuality'])
    plt.xlabel('Time of the day')
    plt.ylabel('Time behind schedule')
    plt.show()

def plotMeanLateness(timetable, hours, line, stop, direction):
    times, means, medians, sd = findMeanPunct(timetable, hours, line)
    plt.bar(times, means, width=1.0, align='edge')
    plt.scatter(times+0.5, medians, c='k')
    plt.scatter(times+0.5, sd, c='g')
    plt.axhline(y=0, color='r', linestyle='-')
    plt.legend(['On time', 'Median', 'Standard deviation', 'Punctuality'])
    plt.title('Histogram for the mean minutes all ' + direction + ' buses leave ' + stop + ' behind schedule for the the hours in the day')
    plt.xlabel('Time of the day')
    plt.ylabel('Time behind schedule/minutes')
    plt.show()

def plotMoreMeanBars(timetable, hours, line, stop, direction):
    times, means, medians, vars = getMoreBars(timetable, hours, line)
    times = [x/4 for x in times]
    plt.bar(times, means, width=0.25, align='edge')
    plt.axhline(y=0, color='r', linestyle='-')
    plt.legend(['On time','Punctuality'])
    plt.title('Histogram for the mean minutes all ' + direction + ' buses leave ' + stop + ' behind schedule for the the hours in the day')
    plt.xlabel('Time of the day')
    plt.ylabel('Time behind schedule/minutes')
    plt.show()

if __name__ == '__main__':
    ''' Parameters to change '''
    filenames = listFilenames()
    busStopName = 'Bristol College Green (P1)'
    # list all the bus lines being considered
    lines = ['4','3']
    # inbound/southbound or outbound/northbound
    direction = 'outbound'
    # Can either find this or put in the lat/longs
    stopLocation = ['51.453000', '-2.600830']
    ''' Code to call - Choose plots wanted '''
    arrivaltimes, times = leaveTimes(filenames, busStopName, lines, direction, stopLocation, False)
    timetable = onlyNeededTimetable(direction, lines, busStopName)
    #plotLatenessHist(timetable, times)
    plotMeanLateness(timetable, times, lines, busStopName, direction)
    #plotMoreMeanBars(timetable, times, lines, busStopName)