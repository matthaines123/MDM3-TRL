
import pandas as pd
import numpy as np
import math

import matplotlib.pyplot as plt
from matplotlib.path import Path

import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM

from io import BytesIO
from PIL import Image
import requests

from visualiseLocationData import getBusLocationsDF, getBusLocationsDict, plotLatLong
from getLocationData import getBusData
from itertools import product

def makeCartopyMap(initial_df):
    '''
    Input dateframe including lats and longs
    Returns a cartopy map
    '''
    if initial_df.shape[0] > 20:
        df = initial_df.head(20)
    else:
        df = initial_df
    lats = list(map(float, df[0]))
    longs = list(map(float, df[1]))

    top, bot = float(df[0].max()), float(df[0].min())
    rgt, lef = float(df[1].min()), float(df[1].max())

    imagery = OSM()

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=imagery.crs)
    ax.set_extent([lef, rgt, bot, top], ccrs.PlateCarree())

    theta = np.linspace(0, 2*np.pi, 100)
    circle_verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = Path.make_compound_path(Path(circle_verts[::-1]), Path(circle_verts*0.1))

    
    
    #rectangle = Path([[-1.1, -0.2], [1, -0.2], [1, 0.3], [-1.1, 0.3]])
    ax.add_image(imagery, 14)
    
    ax.plot(longs, lats, transform=ccrs.PlateCarree(), marker=circle, color='red', markersize=10, linestyle='', alpha=0.5)
    plt.show()

datafeedID = 699

'''
First Bus Bristol = 699
Frome Bus = 3587
Faresaver = 685

'''

if __name__ == '__main__':
    #Get the bus data from the open bus data API
    timestamp, data = getBusData(datafeedID)
    busDict = getBusLocationsDict(data)
    df = getBusLocationsDF(busDict)
    #Convert bus GPS coords to lists of latitudes and longitudes

    #makeMap(lats, longs)
    makeCartopyMap(df)