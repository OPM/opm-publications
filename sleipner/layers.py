#!/usr/bin/env python
import numpy as np
from ecl.eclfile import EclFile
from ecl.grid import EclGrid
from shapely.geometry import Polygon, Point

def layers():
  gridlayers = "SleipnerRefModel_GridLayers.txt"
  layerstxt = np.genfromtxt(gridlayers, dtype=(str, int))
  layers = layerstxt[:,1].astype(np.int)
  shale = layerstxt[:,0] == 'In'  
  caprock = layerstxt[:,0] == 'Ca'
  utsira = layerstxt[:,0] == 'Ut'
  sand = layerstxt[:,0] == 'Sa'
  thick = layerstxt[:,0] == 'Th'
  shale = np.any([shale,caprock,thick],axis=0)
  utsira = np.any([utsira,sand],axis=0)

  cumsum = layers.cumsum()
  layerShale = cumsum[shale]
  layerUtsira = cumsum[utsira]
  numLayers = sum(utsira)
  mapUtsira = np.zeros(np.max(cumsum))
  mapShale = np.zeros(np.max(cumsum))
  for i in range(numLayers):
    for j in range(layerShale[i], layerUtsira[i]):
      mapUtsira[j] = i+1
      
    if (i == 0):
      for j in range(layerShale[i]):
        mapShale[j] = i+1
    else:
      for j in range(layerUtsira[i-1], layerShale[i]):
        mapShale[j] = i+1
  return layerShale, layerUtsira, mapShale, mapUtsira
