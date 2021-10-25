import matplotlib.pyplot as plt
from LoadLocationData import LoadLocationData
from getLineIds import LineIds
import pandas as pd
import numpy as np

def getDictOfLineLatLongTime(matchIDstoLines, LoadLocationData, filename, filenameLines):

    LineLatLongTimeDict = {}
    
    IDsforLines = matchIDstoLines(filename, filenameLines)

    df, dfLines, dataAtTimes = LoadLocationData(filename, filenameLines)
    print(pd.DataFrame(data=dataAtTimes))
    print(pd.DataFrame(data=IDsforLines))

    for key, busId in IDsforLines.items():
        #print(key)
        #print(busId)
        LineLatLongTimeDict.setdefault(key)
        for time, busData in dataAtTimes.items():
            for id, loc in busData.items():
                #append dataAtTimes for id to key that matches with busId
                #line = list(IDsforLines.keys())[list(IDsforLines.values()).index(id)]
                miniTimeLocDict = {}
                if id in busId:
                    locList = id
                miniTimeLocDict[time] = loc
        LineLatLongTimeDict[key] = miniTimeLocDict

    #print(LineLatLongTimeDict)

    return LineLatLongTimeDict

def getIndexOfDF(df, value):
     
    # Empty list
    listOfPos = []
     
    # isin() method will return a dataframe with
    # boolean values, True at the positions
    # where element exists
    result = df.isin([value])
    #result = df[df.str.contains('|'.join(value))]
     
    # any() method will return
    # a boolean series
    seriesObj = result.any()
 
    # Get list of column names where
    # element exists
    columnNames = list(seriesObj[seriesObj == True].index)
    
    # Iterate over the list of columns and
    # extract the row index where element exists
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
 
        for row in rows:
            listOfPos.append((row, col))
             
    # This list contains a list tuples with
    # the index of element in the dataframe
    return listOfPos

def getHoursMins(datetime):
    splitted = [char for char in str(datetime)]
    hour = int(splitted[11]+splitted[12])
    minute = int(splitted[14]+splitted[15])+float(splitted[17]+splitted[18])/60
    
    return hour, minute

def plotStopTimes(filename, locations):

    df = LoadLocationData(filename)

    hours, mins = [], []
    for location in locations:
        LinesTimes = getIndexOfDF(df, location)
        #print(LinesTimes)
        hour, minute = getHoursMins(LinesTimes(1))
        hours.append(hour)
        mins.append(minute)
        plt.scatter(hours, mins, s=10)

plotStopTimes('LocationDataLog19-10-2021,18;16;05RunTime28800.json',[51.476441, -2.699206])
