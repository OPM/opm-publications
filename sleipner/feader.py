#!/usr/bin/env python
import numpy as np
from ecl.eclfile import EclFile
from ecl.grid import EclGrid
from shapely.geometry import Polygon, Point
from layers import layers

# Script that generates input data to ERT for the feaders
# We use a lognorm distribution with mean log(1) and variance log(10)
# for the z permeability of the feader. 
fn = "feaders.tmpl"
fn2 = "feaders.txt"
gridname = 'Sleipner_Reference_Model.grdecl'
DISTR = "LOGNORMAL"
permFeader = np.log(1) #1000
permvarFeader = np.log(100)
#permMinMax = [0.00075, 5000]

feadernames=[]
feadernames.append(('Main_feeder_chimney',[2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7]))
feadernames.append(('NE_feeder_L5_L6_low_confidence', [6],[8]))
feadernames.append(('SW_feeder_L7_L8_low_confidence', [8],[9]))

polys = []
for feadername in feadernames:
  feadertxt = np.genfromtxt(feadername[0], skip_header=16, dtype=(np.float, np.float, np.float, np.int))
  coords = []
  for line in feadertxt:
    if (line[3]==0):
      coords.append((line[0],line[1]))
  
  polys.append(Polygon(coords))

layerShale, layerUtsira, mapShale, mapUtsira = layers()
grid = EclGrid.load_from_grdecl(gridname)
feaders = [ [] for x in range(10)]
for cell in grid.cells():  
  for feadername,poly in zip(feadernames,polys):
    for layerj, ind in zip(feadername[1],feadername[2]):
      if (mapShale[cell.k - 1] != layerj):
        continue  
      if(poly.contains(Point(cell.coordinate))):
        feaders[ind].append(cell.ijk)

f = open(fn, "w")
f2 = open(fn2, "w")
for feadername in feadernames:
  for ind in feadername[2]:
    feader = feaders[ind]
    if (len(feader) > 0):
      f.write("EQUALS \n")
      f.write(" 'PERMZ' ")
      f.write("<FEADER" + str(ind) + "> ")
      boxmins = np.min(feader,axis=0)
      boxmaxs = np.max(feader,axis=0)
      for boxmin,boxmax in zip(boxmins,boxmaxs): 
        f.write(str(boxmin) + " " + str(boxmax) + " ") 
      f.write("/\n/\n\n")
      f2.write("FEADER" + str(ind) + " " + DISTR + " " + str(permFeader) + " " + str(permvarFeader) + "\n")
 

