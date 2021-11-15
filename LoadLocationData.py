import json
import pandas as pd

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



"""
def merge_JsonFiles(filename, outputFilename):
    result = list()
    for f1 in filename:
        with open('Location_Data_files/'+f1, 'r') as infile:
            result.extend(json.load(infile))

    with open('Location_Data_files/'+outputFilename, 'w') as output_file:
        json.dump(result, output_file)

merge_JsonFiles(['LocationDataLog26-10-2021,12;20;15RunTime14400.json','LocationDataLog26-10-2021,19;38;25RunTime25200.json'],'LocationDataLog26-10-2021,19;38;25RunTime39600.json')
merge_JsonFiles(['LineReferences26-10-2021,12;20;47RunTime14400.json','LineReferences26-10-2021,19;40;41RunTime25200.json'],'LineReferences26-10-2021,19;38;25RunTime39600.json')
"""