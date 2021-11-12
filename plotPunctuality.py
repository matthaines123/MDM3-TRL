import matplotlib.pyplot as plt
from calcPunctuality import findLateness, findMeanPunct
from findLeaveTimes import leaveTimes

def plotLatenessHist(timetable, hours):
    lateness = findLateness(timetable, hours)
    plt.bar(hours, lateness, edgecolor='w')
    plt.axhline(y=0, color='r', linestyle='-')
    plt.legend(['On time','Punctuality'])
    plt.xlabel('Time of the day')
    plt.ylabel('Time behind schedule')
    plt.show()

def plotMeanLateness(timetable, hours, line):
    times, means = findMeanPunct(timetable, hours, line)
    plt.bar(times+0.5, means, edgecolor='w')
    plt.axhline(y=0, color='r', linestyle='-')
    plt.legend(['On time','Punctuality'])
    plt.xlabel('Time of the day')
    plt.ylabel('Time behind schedule')
    plt.show()

def produceTimetable():
    timetable = []
    for i in range(45):
        timetable.append(7.96 + 0.25*i)
    return timetable

if __name__ == '__main__':
    ''' Parameters to change '''
    filenames = ['LocationDataLog27-10-2021,19;26;47RunTime32400.json','LocationDataLog19-10-2021,18;16;05RunTime28800.json','LocationDataLog26-10-2021,12;20;15RunTime14400.json','LocationDataLog26-10-2021,19;38;25RunTime25200.json']
    busStopName = 'Filton Avenue, Lockleaze Road'
    line = '73'
    direction = 'inbound'
    ''' Code to call - Choose plots wanted '''
    times = leaveTimes(filenames, busStopName, line, direction)
    timetable = produceTimetable()
    #plotLatenessHist(timetable, times)
    plotMeanLateness(timetable, times, line)