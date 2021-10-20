import os
import xmltodict
import pandas as pd

operatorDict = {}

for filename in os.listdir('FBRI-BRISTOL-2021-09-12-v5-BODS_V1_0'):
    path = 'FBRI-BRISTOL-2021-09-12-v5-BODS_V1_0\%s' % filename
    busName = filename.split('-')[0]
    with open(path, 'r') as xml_obj:
        dict_data = xmltodict.parse(xml_obj.read())
        data = dict_data['TransXChange']
        routes = []
        valid = True
        stops = {}
        
        classes = ['Name', 'Lat', 'Long']
        for stop in data['StopPoints'].items():
            for stopPoint in stop[1]:
                stopRef = stopPoint['StopPointRef']
                stopName = stopPoint['CommonName']
                stops[stopRef] = stopName

        for key, route_sections in data['RouteSections'].items():

            for route in route_sections:
                stopRef = []
                stopsInfo = []
                try:
                    for section in route['RouteLink']:
                        stopRef.append(section['From']['StopPointRef'])
                        stopLat = section['Track']['Mapping']['Location'][0]['Latitude']
                        stopLong = section['Track']['Mapping']['Location'][0]['Longitude']
                        stopName = stops[section['From']['StopPointRef']]
                        stopsInfo.append([stopName, stopLat, stopLong])
                except TypeError:
                    valid = False
            
                
                if valid == True:
                    df = pd.DataFrame(stopsInfo, columns=classes, index=stopRef)
                    routes.append(df)
    if valid == True:
        operatorDict[busName] = routes

print(operatorDict)





            
            


    