import requests
import json
import xmltodict

'''Gets the timetable data from the open data for a particular operator, operator is given
by the dataset ID. This can be found on the gov open data website'''

#First Bus = datasetID: 2877

datasetID = 699
parameters = {
    'operatorName = FirstBus'
}

#Insert api key for the bus data
api_key = 'ab0548a48b728cc95b1e95a76004c8503dcf3c26'

#Connecting to the API
response = requests.get('https://data.bus-data.dft.gov.uk/api/v1/dataset/%i/?api_key=%s' % (datasetID, api_key))

#Checking response, 200 is a success
print(response.status_code)

response

#Nicely printing the JSON file in a readable format
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent = 4)
    print(text)

def dictPrint(obj):
    data = obj.keys()
    print(data)

dictPrint(response.json())
