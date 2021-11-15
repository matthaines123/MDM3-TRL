import pandas as pd

import LoadLocationData
import anprCameraRoutes
import getTrafficData
import matplotlib.pyplot as plt
from calcPunctuality import findLateness, findMeanPunct, getMoreBars
from findLeaveTimes import leaveTimes
from importTimetable import onlyNeededTimetable
from datetime import datetime
from getTrafficData import getTrafficForRange

from scipy.stats import pearsonr
import matplotlib.pyplot as plt



#Defining Constants

FILENAMES = ['LocationDataLog27-10-2021,19;26;47RunTime32400.json','LocationDataLog19-10-2021,18;16;05RunTime28800.json','LocationDataLog26-10-2021,12;20;15RunTime14400.json','LocationDataLog26-10-2021,19;38;25RunTime25200.json']
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
hours, means = findMeanPunct(timetable, times, lines)
rCoeff = pearsonr(speeds, means)
print(rCoeff)
plt.scatter(speeds, means)
plt.show()

