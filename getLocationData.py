import requests
import xmltodict

'''Gets the location data from the open data for a particular operator, operator is given
by the datafeed ID. This can be found on the gov open data website'''

#First Bus = datafeedID: 2905
def getBusData(datafeedID, api_key, lastTimestamp, lastBusData):
    parameters = {
        'operatorName = FirstBus'
    }

    #Insert api key for the bus data
    #api_key = 'ab0548a48b728cc95b1e95a76004c8503dcf3c26'

    #Connecting to the API
    response = requests.get('https://data.bus-data.dft.gov.uk/api/v1/datafeed/%i/?api_key=%s' % (datafeedID, api_key))

    #Checking response, 200 is a success
    if response.status_code != 200:
        print("Error could not access data")
        timestamp = lastTimestamp
        busDataList = lastBusData
    else:

        #Getting data in dictionary form
        dict_data = xmltodict.parse(response.content)
        data = dict_data['Siri']['ServiceDelivery']

        #Get timestamp of data
        timestamp = data['ResponseTimestamp']

        #Get location data for buses
        busDataList = data['VehicleMonitoringDelivery']['VehicleActivity']
    return timestamp, busDataList
