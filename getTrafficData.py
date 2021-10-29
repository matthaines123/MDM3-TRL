import matplotlib.pyplot as plt
from matplotlib.path import Path
import json
from LoadLocationData import LoadLocationData
import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM
import pandas as pd
import numpy as np

def getTrafficGates():
    data = json.load(open("dim-journey-links.json"))
    coordinates = np.zeros((2,2, len(data)))
    for i in range(len(data)):
        coordinates[0, 0, i] = np.array(data[i]['fields']['geo_shape']['coordinates'][0][1])
        coordinates[0, 1, i] = np.array(data[i]['fields']['geo_shape']['coordinates'][0][0])
        coordinates[1, 0, i] = np.array(data[i]['fields']['geo_shape']['coordinates'][-1][1])
        coordinates[1, 1, i] = np.array(data[i]['fields']['geo_shape']['coordinates'][-1][0])
    return coordinates

"""
def main(coordinates):
    imagery = OSM()
    lats = list(map(float, coordinates[:, 1]))
    longs = list(map(float, coordinates[:,0]))
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=imagery.crs)
    ax.set_extent([coordinates[:,0].min(), coordinates[:,0].max(), coordinates[:,1].min(), coordinates[:,1].max()], ccrs.PlateCarree())
    ax.add_image(imagery, 14)

    theta = np.linspace(0, 2*np.pi, 100)
    circle_verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = Path.make_compound_path(Path(circle_verts[::-1]), Path(circle_verts*0.1))

    ax.plot(longs, lats, transform=ccrs.PlateCarree(), marker=circle, color='red', markersize=10, linestyle='', alpha=0.5)
    plt.show()
"""


if __name__ == '__main__':
    coordinates = getTrafficGates()
    print(coordinates[:, :, 5])
    #main(coordinates)