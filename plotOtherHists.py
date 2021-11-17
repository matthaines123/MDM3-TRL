import matplotlib.pyplot as plt
from calcPunctuality import findMeanPunct
from findLeaveTimes import leaveTimes
from importTimetable import onlyNeededTimetable

#files = ['LocationDataLog02-11-2021,19;24;44RunTime32400.json', 'LocationDataLog03-11-2021,12;23;10RunTime14400.json', 'LocationDataLog03-11-2021,15;31;38RunTime10800.json', 'LocationDataLog03-11-2021,18;35;36RunTime10800.json', 'LocationDataLog04-11-2021,18;32;12RunTime7200.json', 'LocationDataLog05-11-2021,11;19;39RunTime10800.json', 'LocationDataLog09-11-2021,18;53;54RunTime25200.json', 'LocationDataLog11-11-2021,11;19;23RunTime10800.json', 'LocationDataLog11-11-2021,18;36;34RunTime25200.json', 'LocationDataLog12-11-2021,18;43;58RunTime36000.json', 'LocationDataLog15-11-2021,12;46;35RunTime14400.json', 'LocationDataLog16-11-2021,13;28;00RunTime18000.json', 'LocationDataLog16-11-2021,18;50;30RunTime18000.json', 'LocationDataLog19-10-2021,18;16;05RunTime28800.json', 'LocationDataLog26-10-2021,12;20;15RunTime14400.json', 'LocationDataLog26-10-2021,19;38;25RunTime25200.json', 'LocationDataLog27-10-2021,19;26;47RunTime32400.json']
busStopName = 'Bristol College Green (P1)'
# list all the bus lines being considered
lines = ['4','3']
# inbound/southbound or outbound/northbound
direction = 'outbound'
# Can either find this or put in the lat/longs
stopLocation = ['51.453000', '-2.600830']
''' Code to call - Choose plots wanted '''
timetable = onlyNeededTimetable(direction, lines, busStopName)

def Days():
    filenames = {'Tuesday':['LocationDataLog02-11-2021,19;24;44RunTime32400.json','LocationDataLog09-11-2021,18;53;54RunTime25200.json','LocationDataLog16-11-2021,13;28;00RunTime18000.json', 'LocationDataLog16-11-2021,18;50;30RunTime18000.json','LocationDataLog19-10-2021,18;16;05RunTime28800.json', 'LocationDataLog26-10-2021,12;20;15RunTime14400.json', 'LocationDataLog26-10-2021,19;38;25RunTime25200.json'],'Wednesday':['LocationDataLog03-11-2021,12;23;10RunTime14400.json', 'LocationDataLog03-11-2021,15;31;38RunTime10800.json', 'LocationDataLog03-11-2021,18;35;36RunTime10800.json','LocationDataLog27-10-2021,19;26;47RunTime32400.json'],'Thursday':['LocationDataLog04-11-2021,18;32;12RunTime7200.json','LocationDataLog11-11-2021,11;19;23RunTime10800.json', 'LocationDataLog11-11-2021,18;36;34RunTime25200.json'],'Friday':['LocationDataLog12-11-2021,18;43;58RunTime36000.json','LocationDataLog05-11-2021,11;19;39RunTime10800.json']}
    for key, value in filenames.items():
        times = leaveTimes(value, busStopName, lines, direction, stopLocation)
        times, means, medians, sd = findMeanPunct(timetable, times, lines)
        plt.bar(times, means, width=1.0, align='edge', alpha=0.2)
    plt.axhline(y=0, color='r', linestyle='-')
    plt.legend(['On time', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
    plt.title('Histogram for the mean minutes all ' + direction + ' buses leave ' + busStopName + ' behind schedule for the the hours in the day. For weekdays.')
    plt.xlabel('Time of the day')
    plt.ylabel('Time behind schedule/minutes')
    plt.show()

def Students():
    filenames = {'Not Reading week':['LocationDataLog09-11-2021,18;53;54RunTime25200.json', 'LocationDataLog11-11-2021,11;19;23RunTime10800.json', 'LocationDataLog11-11-2021,18;36;34RunTime25200.json', 'LocationDataLog12-11-2021,18;43;58RunTime36000.json', 'LocationDataLog15-11-2021,12;46;35RunTime14400.json', 'LocationDataLog16-11-2021,13;28;00RunTime18000.json', 'LocationDataLog16-11-2021,18;50;30RunTime18000.json', 'LocationDataLog19-10-2021,18;16;05RunTime28800.json', 'LocationDataLog26-10-2021,12;20;15RunTime14400.json', 'LocationDataLog26-10-2021,19;38;25RunTime25200.json', 'LocationDataLog27-10-2021,19;26;47RunTime32400.json'],'Reading week':['LocationDataLog02-11-2021,19;24;44RunTime32400.json', 'LocationDataLog03-11-2021,12;23;10RunTime14400.json', 'LocationDataLog03-11-2021,15;31;38RunTime10800.json', 'LocationDataLog03-11-2021,18;35;36RunTime10800.json', 'LocationDataLog04-11-2021,18;32;12RunTime7200.json', 'LocationDataLog05-11-2021,11;19;39RunTime10800.json']}
    for key, value in filenames.items():
        times = leaveTimes(value, busStopName, lines, direction, stopLocation)
        times, means, medians, sd = findMeanPunct(timetable, times, lines)
        plt.bar(times, means, width=1.0, align='edge', alpha=0.2)
    plt.axhline(y=0, color='r', linestyle='-')
    plt.legend(['On time', 'Full cohort', 'Reading week'])
    plt.title('Histogram for the mean minutes all ' + direction + ' buses leave ' + busStopName + ' behind schedule for the the hours in the day. For reading week and outside of this week.')
    plt.xlabel('Time of the day')
    plt.ylabel('Time behind schedule/minutes')
    plt.show()

def ClockChange():
    filenames = {'Before clock change':['LocationDataLog19-10-2021,18;16;05RunTime28800.json', 'LocationDataLog26-10-2021,12;20;15RunTime14400.json', 'LocationDataLog26-10-2021,19;38;25RunTime25200.json', 'LocationDataLog27-10-2021,19;26;47RunTime32400.json'], 'After clock change':['LocationDataLog02-11-2021,19;24;44RunTime32400.json', 'LocationDataLog03-11-2021,12;23;10RunTime14400.json', 'LocationDataLog03-11-2021,15;31;38RunTime10800.json', 'LocationDataLog03-11-2021,18;35;36RunTime10800.json', 'LocationDataLog04-11-2021,18;32;12RunTime7200.json', 'LocationDataLog05-11-2021,11;19;39RunTime10800.json', 'LocationDataLog09-11-2021,18;53;54RunTime25200.json', 'LocationDataLog11-11-2021,11;19;23RunTime10800.json', 'LocationDataLog11-11-2021,18;36;34RunTime25200.json', 'LocationDataLog12-11-2021,18;43;58RunTime36000.json', 'LocationDataLog15-11-2021,12;46;35RunTime14400.json', 'LocationDataLog16-11-2021,13;28;00RunTime18000.json', 'LocationDataLog16-11-2021,18;50;30RunTime18000.json']}
    for key, value in filenames.items():
        times = leaveTimes(value, busStopName, lines, direction, stopLocation)
        times, means, medians, sd = findMeanPunct(timetable, times, lines)
        plt.bar(times, means, width=1.0, align='edge', alpha=0.2)
    plt.axhline(y=0, color='r', linestyle='-')
    plt.legend(['On time', 'Before clock change', 'After clock change'])
    plt.title('Histogram for the mean minutes all ' + direction + ' buses leave ' + busStopName + ' behind schedule for the the hours in the day. For the clock change.')
    plt.xlabel('Time of the day')
    plt.ylabel('Time behind schedule/minutes')
    plt.show()