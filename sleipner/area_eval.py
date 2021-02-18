#!/usr/bin/env python
import sys
import numpy as np
from ecl.eclfile import EclFile
from ecl.grid import EclGrid
import datetime
from layers import layers

#Computes the areas of the top surface of the cells on the top of the sand layers with saturation above sgLimit the 1.9.2010
caseData = datetime.datetime( 2010 , 9 , 1 )
outputFileName = "plume_areas_0.out"
sgLimit = 0.1

caseName = sys.argv[1]
layerShale, layerUtsira, mapShale, mapUtsira = layers()
numLayers = len(layerUtsira)
gridname = caseName + '.EGRID'
grid = EclGrid(gridname)
rstname =  caseName + ".UNRST"
rst = EclFile(rstname)
sgass = rst.restart_get_kw( "SGAS" ,caseData )
areas = np.zeros(numLayers)
for cell, sg in zip(grid.cells(), sgass):
  for layer in range(numLayers):
    # sum cell areas (volume/hight) of the first row of cells in the layer
    # with sg > sgLimit   
    if(sg > sgLimit and cell.k == layerShale[layer]):
      areas[layer] += cell.volume / cell.dz 

f = open(outputFileName, "w")
for area in areas:
  f.write(str(area) + "\n")

f.close()
