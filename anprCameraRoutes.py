import folium
import osmnx as ox
import networkx as nx
import json
import itertools
import warnings
import math
import numpy as np
from IPython.display import display

warnings.filterwarnings("ignore", category=UserWarning) 

ANPRFILE = 'dim-journey-links.json'

def plotRoutes(coordsDict):
    counter = 0
    routes = {}
    ox.config(use_cache=True, log_console=False)
    #coordsDict2 = dict(itertools.islice(coordsDict.items(), limit))
    for key, coord in coordsDict.items():
        print(counter)
        try:
            G = ox.graph_from_point([coord[0][1], coord[0][0]], dist=1000, network_type='drive')

            G = ox.speed.add_edge_speeds(G)
            G = ox.speed.add_edge_travel_times(G)

            def plotDot(point):
   
                folium.CircleMarker(location=[point[0], point[1]],
                        radius=2,
                        weight=5).add_to(route_map)

            start = ox.get_nearest_node(G, [coord[0][1], coord[0][0]])
            end = ox.get_nearest_node(G, [coord[1][1], coord[1][0]])

            route = nx.shortest_path(G, start, end, 'travel_time')

            bbox = getbboxOfSection(route, G)


            route_map = ox.plot_route_folium(G, route)
            plotDot([51.440739, -2.574904])
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

def getDistanceToVec(route, busCoord):
    '''
    Input: route where bus is in bbox, coord of bus
    '''
    coordPairs = []
    coords = route[0]
    for i in range(0, len(coords[0])):
        coordPairs.append([coords[0][i], coords[1][i]])
    minDist = math.inf
    minPoints = None 
    for i in range(0, len(coordPairs)-1):
        
        p1 = np.asarray(coordPairs[i])
        p2 = np.asarray(coordPairs[i+1])
        p3 = np.asarray(busCoord)
        dist = np.linalg.norm(np.cross(p2-p1, p1 - p3))/np.linalg.norm(p2-p1)
        if dist < minDist:
            minDist = dist
            minPoints = [p2, p1]
    return minDist, minPoints

def displayRoadSection(coordDict, routeDict, name):
    for roadName, coords in coordDict.items():
        if (name in roadName) or (name == 'all'):
            mapName = str(roadName+'_Map.html')
            try:
                mapGraph = routeDict[roadName][1]
                mapGraph.save('anprSections/'+mapName.replace(':','_').replace('/', '_').replace(' ','_'))
            except KeyError:
                pass

def getANPRCoords(file, limit):
    f = open(file)
    data = json.load(f)
    coordDict = {}
    for section in data[:limit]:
        coords = section['fields']['geo_shape']['coordinates']
        name = section['fields']['journeyend'] + ':' + section['fields']['journeystartdirectiondesc']
        coordDict[name] = [coords[0], coords[-1]]

    return coordDict


if __name__ == '__main__':
    anprCoords = getANPRCoords(ANPRFILE, 3)
    routes = plotRoutes(anprCoords)
    road = 'Bath'
    for roadName, coords in routes.items():
        if road in roadName:
            dist, points = getDistanceToVec(routes[roadName], [51.440739, -2.574904])
            print(roadName, dist,points)
    displayRoadSection(anprCoords, routes, road)
    