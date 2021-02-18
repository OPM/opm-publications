#!/usr/bin/env python
import numpy as np
from shapely.geometry import Polygon

## computes the areas of the observed plumes
feaderpath = 'Sleipner_Plumes_Boundaries/data/'
numLayers = 9
filename = 'plume_obs_data.txt'
areas = []
for layer in range(numLayers):
  feadername = feaderpath + "L" + str(layer+1)
  feadertxt = np.genfromtxt(feadername, skip_header=16, dtype=(np.float, np.float, np.float, np.int))
  poly = Polygon([])
  for i in range(4):
    coords = []
    for line in feadertxt:
      if (line[3]==i):
        coords.append((line[0],line[1]))
    
    polyNew = Polygon(coords)
    if(not polyNew.is_empty and not polyNew.within(poly)):
      poly = poly.union(polyNew)

  areas.append(poly.area)

  
f = open(filename, "w")
for area in areas:
  deviation = area*0.1;
  f.write(str(area) + " " + str(deviation) + "\n")

f.close()
  