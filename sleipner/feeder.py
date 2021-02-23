#!/usr/bin/env python
import numpy as np
from ecl.eclfile import EclFile
from ecl.grid import EclGrid
from shapely.geometry import Polygon, Point
from layers import layers

# Script that generates input data to ERT for the feeders
# We use a lognorm distribution with mean log(1) and variance log(10)
# for the z permeability of the feeder. 
fn = "feeders.tmpl"
fn2 = "feeders.txt"
gridname = 'Sleipner_Reference_Model.grdecl'
DISTR = "LOGNORMAL"
permfeeder = np.log(1) #1000
permvarfeeder = np.log(100)
#permMinMax = [0.00075, 5000]

feedernames=[]
feedernames.append(('Main_feeder_chimney',[2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7]))
feedernames.append(('NE_feeder_L5_L6_low_confidence', [6],[8]))
feedernames.append(('SW_feeder_L7_L8_low_confidence', [8],[9]))

polys = []
for feedername in feedernames:
  feedertxt = np.genfromtxt(feedername[0], skip_header=16, dtype=(np.float, np.float, np.float, np.int))
  coords = []
  for line in feedertxt:
    if (line[3]==0):
      coords.append((line[0],line[1]))
  
  polys.append(Polygon(coords))

layerShale, layerUtsira, mapShale, mapUtsira = layers()
grid = EclGrid.load_from_grdecl(gridname)
feeders = [ [] for x in range(10)]
for cell in grid.cells():  
  for feedername,poly in zip(feedernames,polys):
    for layerj, ind in zip(feedername[1],feedername[2]):
      if (mapShale[cell.k - 1] != layerj):
        continue  
      if(poly.contains(Point(cell.coordinate))):
        feeders[ind].append(cell.ijk)

f = open(fn, "w")
f2 = open(fn2, "w")
for feedername in feedernames:
  for ind in feedername[2]:
    feeder = feeders[ind]
    if (len(feeder) > 0):
      f.write("EQUALS \n")
      f.write(" 'PERMZ' ")
      f.write("<feeder" + str(ind) + "> ")
      boxmins = np.min(feeder,axis=0)
      boxmaxs = np.max(feeder,axis=0)
      for boxmin,boxmax in zip(boxmins,boxmaxs): 
        f.write(str(boxmin) + " " + str(boxmax) + " ") 
      f.write("/\n/\n\n")
      f2.write("FEEDER" + str(ind) + " " + DISTR + " " + str(permfeeder) + " " + str(permvarfeeder) + "\n")
 

