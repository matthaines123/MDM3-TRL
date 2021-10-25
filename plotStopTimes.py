import matplotlib.pyplot as plt
from LoadLocationData import LoadLocationData
from getLineIds import LineIds

def getSingleLine(df, line):

    AllLineIds = LineIds()
    IdsForLine = AllLineIds[line]
    dfLine = df.loc[IdsForLine]

    return dfLine

def getTimeFromLocation(filename, locations, line):
    accuracy = 4
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

def getHoursMins(datetime):
    splitted = [char for char in str(datetime)]
    minute = int(splitted[14]+splitted[15])+float(splitted[17]+splitted[18])/60
    hour = int(splitted[11]+splitted[12])+minute/60
    
    return hour, minute

def useAllDaysData(code):

    some = code

    return some

def plotStopTimes(filename, locations, line):

    times = getTimeFromLocation(filename, locations, line)
    hours, mins = [], []
    for time in times:
        hour, min = getHoursMins(time)
        hours.append(hour)
        mins.append(min)
    plt.scatter(hours, mins, s=10)
    plt.xlabel('Hour of day')
    plt.ylabel('Minute')
    plt.show()

plotStopTimes('LocationDataLog19-10-2021,18;16;05RunTime28800.json',[[51.453000, -2.600830]],'2a')
