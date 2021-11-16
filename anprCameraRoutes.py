import folium
import osmnx as ox
import networkx as nx
import json
import itertools
import warnings
import math
import numpy as np
from os import listdir
from os.path import isfile, join
import xmltodict
from IPython.display import display
#from plotStopTimes import getDecimalTime, getMinute
from findLeaveTimes import leaveTimes
from statistics import mean

warnings.filterwarnings("ignore", category=UserWarning) 



def plotRoutes(coordsDict):
    counter = 0
    routes = {}
    ox.config(use_cache=True, log_console=False)
    #coordsDict2 = dict(itertools.islice(coordsDict.items(), limit))
    for key, coord in coordsDict.items():
        print(counter)
        try:
            G = ox.graph_from_point([coord[0][1], coord[0][0]], dist=1000, simplify=False, network_type='drive')

            G = ox.speed.add_edge_speeds(G)
            G = ox.speed.add_edge_travel_times(G)                

            start = ox.get_nearest_node(G, [coord[0][1], coord[0][0]])
            end = ox.get_nearest_node(G, [coord[-1][1], coord[-1][0]])

            #D = ox.utils_graph.get_digraph(G, weight="travel_time")

            route = nx.shortest_path(G, start, end)

            bbox = getbboxOfSection(route, G)

            route_map = ox.plot_route_folium(G, route)
            folium.CircleMarker(location=[51.440739, -2.574904],
                        radius=2,
                        weight=5).add_to(route_map)
            routes[key] = [bbox, route_map]
            counter += 1
        except nx.exception.NetworkXNoPath:
            counter += 1

    return routes

def getbboxOfSection(route, G):
    longs = []
    lats = []
    for node in route:
        longs.append(G.nodes[node]['x'])
        lats.append(G.nodes[node]['y'])

    bbox = [lats, longs]
    return bbox

def checkBBox(coord1, coord2, busCoord):
        x1, y1 = coord1
        x2, y2 = coord2
        x = float(busCoord[0])
        y = float(busCoord[1])
        if float(x1) > float(x) > float(x2) or float(x1) < float(x) < float(x2):
            if float(y1) > float(y) > float(y2) or float(y1) < float(y) < float(y2):
                return True
        return False

def getDistanceToVec(route, busCoord):
    '''
    Input: route where bus is in bbox, coord of bus
    '''
    coordPairs = []
    coords = route[0]
    
    

    if checkBBox([coords[0][0], coords[1][0]], [coords[0][-1], coords[1][-1]], busCoord):
        for i in range(0, len(coords[0])):
            coordPairs.append([coords[0][i], coords[1][i]])
        points = None 
        for i in range(0, len(coordPairs)-1):
            if checkBBox(coordPairs[i], coordPairs[i+1], busCoord): 
                return [coordPairs[i], coordPairs[i+1]]
    return False


def displayRoadSection(coordDict, routeDict, name, points):
    for roadName, coords in coordDict.items():
        if (name in roadName) or (name == 'all'):
            mapName = str(roadName+'_Map.html')
            try:
                mapGraph = routeDict[roadName][1]
                folium.CircleMarker(location=[points[0][1], points[0][0]],radius=2,weight=5).add_to(mapGraph)
                folium.CircleMarker(location=[points[1][1], points[1][0]],radius=2,weight=5).add_to(mapGraph)
                mapGraph.save('anprSections/'+mapName.replace(':','_').replace('/', '_').replace(' ','_'))
            except KeyError:
                pass

def getANPRCoords(file, name):
    f = open(file)
    data = json.load(f)
    coordDict = {}
    lengths = {}
    for section in data: 
        coords = section['fields']['geo_shape']['coordinates']
        sectionName = section['fields']['journeyend'] + ':' + section['fields']['journeystartdirectiondesc']
        if name.lower() in sectionName.lower(): 
            coordDict[sectionName] = coords
            lengths[sectionName] = section['fields']['length_m']
    return coordDict, lengths

def getTimeInGate(startTime, endTime):
    sTime = getDecimalTime(startTime)
    eTime = getDecimalTime(endTime)
    duration = (60*getMinute(eTime-sTime))
    return duration

def getDictBusIds(busDict):
    newDict = {}

    for time, busesAtTimes in busDict.items():
        timeDict = {}
        for busLocation in busesAtTimes:
            busID = busLocation[0]
            location = busLocation[1]
            timeDict[time] = location
            if busID in newDict.keys():
                newDict[busID].append(timeDict)
            else:
                newDict[busID] = [timeDict]

    return newDict

def checkBusIsInGate(busCoords, anprFile, road):
    accuracy = 4
    busSpeed = True
    busInGate = {}
    currentBuses = {}
    anprCoords, lengths = getANPRCoords(anprFile, road)
    routes = plotRoutes(anprCoords)
    busIdLocations = getDictBusIds(busCoords)
    for time, busesAtTime in busCoords.items():
        for bus in busesAtTime:
            for routeName, routeInfo in routes.items():
                routeLocation = routeInfo[0]
                point1 = [min(routeLocation[0]), min(routeLocation[1])]
                point2 = [max(routeLocation[0]), max(routeLocation[1])]
                onRoute = checkBBox(point1, point2, bus[1])
                if onRoute:
                    sectionsGoneThrough = {}
                    busOnRoad = False
                    #Iterate over each section
                    for i in range(0, len(routeLocation[0])-1):
                        currentBusID = busIdLocations[bus[0]]
                        
                        for timeLocation in currentBusID:
                            point1 = [routeLocation[0][i], routeLocation[1][i]]
                            point2 = [routeLocation[0][i+1], routeLocation[1][i+1]]
                            busCoord = list(timeLocation.values())[0]
                            busTime = list(timeLocation.keys())[0]
                            onSection = checkBBox(point1, point2, busCoord)
        
                            if onSection:
                                busOnRoad = True
                                if point1[0] not in sectionsGoneThrough.keys():
                                    sectionsGoneThrough[point1[0]] = [busTime]

                                break
                                
                            elif (onSection == False and busOnRoad == True):
                                if len(sectionsGoneThrough.keys()) > 1:
                                    print("RouteDone")
                                    print(BusesSections)
                                    firstPoint = sectionsGoneThrough[0][1]
                                    lastPoint = sectionsGoneThrough[-1][1]

                                    G = ox.graph_from_point(firstPoint, dist=1000, network_type='drive')
                                    G = ox.speed.add_edge_speeds(G)
                                    G = ox.speed.add_edge_travel_times(G)

                                    route = nx.shortest_path_length(G, firstPoint, lastPoint)
                                    print(route)
                                    break
                                else:
                                    break
    
                            

                            

        #Check bus is in bbox of general anpr zone
    




    '''else:
        points = getDistanceToVec(routes[roadName], location[1])
        if points != False:
            if roadName in busInGate.keys():
                busInGate[roadName].append(time)
            else:
                busInGate[roadName] = [time]'''

def getDistanceBetweenStops(stop1, stop2, lines, ids):
    lineDistances = {}
    if ids == None:
        stopCodes = [None, None]
        for line in lines:
            filename = [file for file in listdir('FBRI-BRISTOL-2021-09-12-v5-BODS_V1_0') if file.split('-')[0] == line]
            path = 'FBRI-BRISTOL-2021-09-12-v5-BODS_V1_0\%s' % filename[0]
            with open(path, 'r') as xml_obj:
                dict_data = xmltodict.parse(xml_obj.read())['TransXChange']
                
                stoppoints = dict_data['StopPoints']
                for key, stoppoint in stoppoints.items():
                    for point in stoppoint:
                        if stop1 in point['CommonName']:
                            stopCodes[0] = point['StopPointRef']
                        elif stop2 in point['CommonName']:
                            stopCodes[1] = point['StopPointRef']

                print(stopCodes)
    else:
        for line in lines:
            filename = [file for file in listdir('FBRI-BRISTOL-2021-09-12-v5-BODS_V1_0') if file.split('-')[0] == line]
            path = 'FBRI-BRISTOL-2021-09-12-v5-BODS_V1_0\%s' % filename[0]
            with open(path, 'r') as xml_obj:
                dict_data = xmltodict.parse(xml_obj.read())['TransXChange']
                routeSection = dict_data['RouteSections']['RouteSection'][0]
                for sectionList in routeSection['RouteLink']:
                    if sectionList['From']['StopPointRef'] == ids[0]:
                        lineDistances[line] = sectionList['Distance']
    #print(lineDistances[line[0]])
    return lineDistances[line[0]]

def getTimesBetweenStops(stop1, stop2, lines, ids, filenames, stopLocation, direction, timeRange):
    timediffs = {}


    times1 = leaveTimes(filenames, stop1, lines, direction, stopLocation[0])
    times2 = leaveTimes(filenames, stop2, lines, direction, stopLocation[1])
    for line, times in times1.items():
        i1, i2 = 0, 0
        if len(times1[line]) > len(times2[line]):
            time1Bigger = True
        else:
            time1Bigger = False
        while i1 < len(times1[line]) and i2 < len(times2[line]):
            timeDiff = abs(times1[line][i1] - times2[line][i2])
            if timeDiff > 0.5:
                oldTimeDiff = timeDiff
                if time1Bigger:
                    if (i1 + 1) < len(times1[line]):
                        newTimeDiff = abs(times1[line][i1+1] - times2[line][i2])
                else:
                    if (i2 + 1) < len(times2[line]):
                        newTimeDiff = abs(times1[line][i1] - times2[line][i2+1])
                if newTimeDiff > oldTimeDiff:
                    timeDiff = oldTimeDiff
                else:
                    timeDiff = newTimeDiff
                    if time1Bigger:
                        i1 += 1
                    else:
                        i2 += 1
            hour = int(times1[line][i1] // 1)
            if hour in timediffs.keys():
                timediffs[hour].append(timeDiff)
            else:
                timediffs[hour] = [timeDiff]
            i1 += 1
            i2 += 1
    meanDiffs = {}
    for i in range(timeRange[0], timeRange[1]):
        meanDiffs[i] = -1

    for time, diffs in timediffs.items():
        meanDiffs[time] = mean(diffs)
    #print(meanDiffs)
    #print(times2)
    return meanDiffs.values()


if __name__ == '__main__':

    #getTimeInGate('2021-10-20T19:57:27.342845+00:00', '2021-10-20T20:58:56.342845+00:00')
    filenames = ['LocationDataLog27-10-2021,19;26;47RunTime32400.json','LocationDataLog19-10-2021,18;16;05RunTime28800.json','LocationDataLog26-10-2021,12;20;15RunTime14400.json','LocationDataLog26-10-2021,19;38;25RunTime25200.json']
    #filenames = ['LocationDataLog27-10-2021,19;26;47RunTime32400.json','LocationDataLog19-10-2021,18;16;05RunTime28800.json','LocationDataLog26-10-2021,12;20;15RunTime14400.json','LocationDataLog26-10-2021,19;38;25RunTime25200.json']
    #filenames = listdir('Location_Data_files')

    ANPRFILE = 'dim-journey-links.json'
    road = 'Queen'
    stop1 = 'College Green'
    stop2 = 'The Centre'
    lines = ['4', '3']
    direction = 'outbound'
    ids = ['0100BRP90326', '0100BRP90337']
    timeRange = [8, 20]
    stopLocation = [['51.453420', '-2.601350'],['51.454920', '-2.596850']]

    times = getTimesBetweenStops(stop1, stop2, lines, ids, filenames, stopLocation, timeRange)
    distance = getDistanceBetweenStops(stop1, stop2, lines, ids)

    
    busSpeeds = [float(distance)/(time*1609) for time in times]
    print(busSpeeds)
