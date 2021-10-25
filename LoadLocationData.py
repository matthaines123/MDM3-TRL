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

def merge_JsonFiles(filename, outputFilename):
    result = list()
    for f1 in filename:
        with open(f1, 'r') as infile:
            result.extend(json.load(infile))

    with open(outputFilename, 'w') as output_file:
        json.dump(result, output_file)