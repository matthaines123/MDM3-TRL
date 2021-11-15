import pandas as pd

import LoadLocationData
import anprCameraRoutes
import getTrafficData



#Defining Constants
FILENAMES = ['LocationDataLog19-10-2021,18;16;05RunTime28800.json']

ANPRFILENAME = 'dim-journey-links.json'

#Defining variables
roadName = 'Anchor'
lines = []

busLocations = LoadLocationData.getBusLocations(FILENAMES)
busInGates = anprCameraRoutes.checkBusIsInGate(busLocations, ANPRFILENAME, roadName)



print(busInGates)
