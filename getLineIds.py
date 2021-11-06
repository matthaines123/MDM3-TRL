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

    LineRefDF = LoadFile('LineReferences26-10-2021,19;40;41RunTime25200.json')
    LineRefs = LineRefDF.iloc[:,0]
    LineRefs = LineRefs.dropna(axis=0)
    LineRefDict = defaultdict(list)
    for i in range(len(LineRefs)-1):
        LineRefDict[LineRefs[i][0]].append(LineRefs.index.values[i])

    return LineRefDict