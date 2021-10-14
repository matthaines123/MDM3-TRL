
import pandas as pd
import numpy as np
import math

import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import requests

from visualiseLocationData import getBusLocationsDF, getBusLocationsDict, plotLatLong
from getLocationData import getBusData
from itertools import product

datafeedID = 685

'''
First Bus Bristol = 699
Frome Bus = 3587
Faresaver = 685

'''
#Get the bus data from the open bus data API
timestamp, data = getBusData(datafeedID)
busDict = getBusLocationsDict(data)
df = getBusLocationsDF(busDict)

#Convert bus GPS coords to lists of latitudes and longitudes
lats = list(map(float, df[0]))
longs = list(map(float, df[1]))
URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png".format

#Map settings
TILE_SIZE = 256
zoom = 13

def point_to_pixels(lon, lat, zoom):
    '''
    convert gps coordinates to tile coordinate on OSM website
    '''
    r = math.pow(2, zoom) * TILE_SIZE
    lat = math.radians(lat)

    x = int((lon + 180.0) / 360.0 * r)
    y = int((1.0 - math.log(math.tan(lat) + (1.0 / math.cos(lat))) / math.pi) / 2.0 * r)

    return x, y

#Find the min and max bus gps locations
top, bot = float(df[0].max()), float(df[0].min())
rgt, lef = float(df[1].min()), float(df[1].max())

#Convert these points to tiles
x0, y0 = point_to_pixels(lef, top, zoom)
x1, y1 = point_to_pixels(rgt, bot, zoom)
x0_tile, y0_tile = int(x0 / TILE_SIZE), int(y0 / TILE_SIZE)
x1_tile, y1_tile = math.ceil(x1 / TILE_SIZE), math.ceil(y1 / TILE_SIZE)

#Check how many tiles are needed for visual, more tiles takes longer
print((x1_tile - x0_tile) * (y1_tile - y0_tile))
assert (x1_tile - x0_tile) * (y1_tile - y0_tile) < 200, "That's too many tiles!"

#Create a map of all the tiles together
img = Image.new('RGB', (
    (x1_tile - x0_tile) * TILE_SIZE,
    (y1_tile - y0_tile) * TILE_SIZE))

# loop through every tile inside our bounded box
for x_tile, y_tile in product(range(x0_tile, x1_tile), range(y0_tile, y1_tile)):
    with requests.get(URL(x=x_tile, y=y_tile, z=zoom)) as resp:
        tile_img = Image.open(BytesIO(resp.content))

    # add each tile to the full size image
    img.paste(
        im=tile_img,
        box=((x_tile - x0_tile) * TILE_SIZE, (y_tile - y0_tile) * TILE_SIZE))

#Plot map with buses ontop
fig, ax = plt.subplots()
ax.scatter(longs, lats, c='red', s=10)
ax.imshow(img, extent=(lef, rgt, bot, top))

plt.show()
