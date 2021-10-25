import json
import pandas as pd
from collections import defaultdict

def LoadFile(filename):

    ''' Loads the saved live location data, output as a dataframe '''

    if '.json' in filename:
        filename = filename
    else:
        filename = filename + '.json'

    with open('Location_Data_files/' + filename, 'r') as fp:
        dataAtTimes = json.load(fp)
        df = pd.DataFrame(data = dataAtTimes)

    return df

def LineIds():

    LineRefDF = LoadFile('LineReferences20-10-2021,20;58;28RunTime60.json')
    LineRefs = LineRefDF['2021-10-20T19:57:27.342845+00:00']
    LineRefDict = defaultdict(list)
    for i in range(468):
        LineRefDict[LineRefs[i][0]].append(LineRefs.index.values[i])

    return LineRefDict