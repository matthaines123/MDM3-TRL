import json
import pandas as pd
from os import listdir
from os.path import isfile, join

def LoadLocationData(filename):

    ''' Loads the saved live location data, output as a dataframe '''

    if '.json' in filename:
        filename = filename
    else:
        filename = filename + '.json'

    with open('Location_Data_files/' + filename, 'r') as fp:
        dataAtTimes = json.load(fp)
        df = pd.DataFrame(data = dataAtTimes)

    return df

def LoadAllLocationData(filenames):

    df = {}
    
    for filename in filenames:
        if '.json' in filename:
            filename = filename
        else:
            filename = filename + '.json'

        with open('Location_Data_files/' + filename, 'r') as fp:
            dataAtTimes = json.load(fp)
            dffile = pd.DataFrame(data = dataAtTimes)

            df.append(dffile)

    return df

def getBusLocations(filenames):
    busLocations = {}
    for dataFile in filenames:
        df = LoadLocationData(dataFile)
        busDict = df.to_dict()
        for time, bus in busDict.items():
            for busID, location in bus.items():
                if type(location) == list:
                    if time in busLocations.keys():
                        locationsList = busLocations[time]
                        busLocations[time].append([busID, location])
                    else:
                        busLocations[time] = [[busID, location]]
    return busLocations

def listFilenames():
    filenames = [f for f in listdir('Location_Data_files/') if isfile(join('Location_Data_files/', f))]
    filenames.pop(0)
    return filenames