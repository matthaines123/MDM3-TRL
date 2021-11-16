import pandas as pd
import anprCameraRoutes
import getTrafficData
import matplotlib.pyplot as plt
from calcPunctuality import findMeanPunct
from findLeaveTimes import leaveTimes
from importTimetable import onlyNeededTimetable
from datetime import datetime
from getTrafficData import getTrafficForRange
from LoadLocationData import listFilenames
from scipy.stats import pearsonr
import matplotlib.pyplot as plt



#Defining Constants

FILENAMES = listFilenames()
ANPRFILENAME = 'dim-journey-links.json'

#Defining variables
roadName = 'Anchor'
lines = ['4','3']
direction = 'outbound'
busStopName = 'Bristol College Green (P1)'
stopLocation = ['51.453000', '-2.600830']
timeRange = [8, 20]

date = datetime(2021, 10, 19, timeRange[0])
speeds = getTrafficForRange(timeRange, roadName, date)

times = leaveTimes(FILENAMES, busStopName, lines, direction, stopLocation)
timetable = onlyNeededTimetable(direction, lines, busStopName)
hours, means, medians, vars = findMeanPunct(timetable, times, lines)
rCoeff = pearsonr(speeds, means)
print(rCoeff)
plt.scatter(speeds, means)
plt.show()

