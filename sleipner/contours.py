#!/usr/bin/env python
import numpy as np
from ecl.eclfile import EclFile
from ecl.grid import EclGrid
from shapely.geometry import Polygon, Point, MultiPoint
import skfmm
import datetime
import matplotlib.pyplot as plt
import sys

path = sys.argv[1]
casename = sys.argv[2]
relnr = sys.argv[3]
iternr = sys.argv[4]

rstname = path + "/realisation-" + relnr + "/iter-" + iternr + "/" +casename +relnr + ".UNRST"
figname = casename + "-" + relnr + "-" + iternr +"-"
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
layerTOP = cumsum[shale]
layerBOT = cumsum[utsira]
numLayers = sum(utsira)
map = np.zeros(np.max(cumsum))
for i in range(1,numLayers):
  for j in range(layerTOP[i], layerBOT[i]):
    map[j]=i

gridname = 'Sleipner_Reference_Model.grdecl'
grid = EclGrid.load_from_grdecl(gridname)
rst = EclFile(rstname)
sgas2010 = rst.restart_get_kw( "SGAS" , datetime.datetime( 2010 , 12 , 1 ))
doPlot = True
feaderpath = 'Sleipner_Plumes_Boundaries/data/'

for layer in range(numLayers):
  legend = []
  coords = []
  xc = []
  yc = []
  val = []
  for cell, sg in zip(grid.cells(), sgas2010):
    if (cell.k == layerTOP[layer]):
      xc.append(cell.coordinate[0])
      yc.append(cell.coordinate[1])
      val.append(sg)
    
    if(sg > 0.1 and cell.k == layerTOP[layer]):
      #print(cell.coordinate[0:2])
      coords.append(Point(cell.coordinate   [0:2])) 

  #plume_polygon = MultiPoint(coords).convex_hull
  #print(tmp.area)
  #if (doPlot):
    #x,y = plume_polygon.exterior.xy
    #plt.plot(x,y)
  
  if (True):
    cs = plt.tricontour(xc, yc, val, levels=[0.1], linewidths=0.5, colors='k')
    for col in cs.collections:
    # Loop through all polygons that have the same intensity level
      for contour_path in col.get_paths(): 
        # Create the polygon for this intensity level
        # The first polygon in the path is the main one, the following ones are "holes"
        for ncp,cp in enumerate(contour_path.to_polygons()):
            x = cp[:,0]
            y = cp[:,1]
            new_shape = Polygon([(i[0], i[1]) for i in zip(x,y)])
            if ncp == 0:
                plume_polygon = new_shape
            else:
                # Remove the holes if there are any
                plume_polygon = plume_polygon.difference(new_shape)
                # Can also be left out if you want to include all rings

        # do something with polygon
        if(not plume_polygon.is_empty):
          print("sim res area " + str(plume_polygon.area))
          x,y = plume_polygon.exterior.xy
          plt.plot(x,y)
          plt.gca().set_aspect('equal', adjustable='box')
          legend.append("sim" + str(len(legend)))

  feadername = feaderpath + "L" + str(layer+1)
  feadertxt = np.genfromtxt(feadername, skip_header=16, dtype=(np.float, np.float, np.float, np.int))
  for i in range(4):
    coords = []
    for line in feadertxt:
      if (line[3]==i):
        coords.append((line[0],line[1]))
 
    poly = Polygon(coords)
    if (not poly.is_empty and doPlot):
      x,y = poly.exterior.xy
      plt.plot(x,y)
      plt.gca().set_aspect('equal', adjustable='box')
      legend.append("data" + str(i))
      print("data area " + str(poly.area))

  if(not poly.is_simple):
    poly = poly.buffer(0)
    #plt.savefig("test" + str(layer+1) + ".png")
    #plt.close()
    #continue
    
  print(str(layer+1))
  if (False):
    inter = poly.intersection(plume_polygon)
    if(not inter.is_empty):
      if (not inter.is_simple):
        inter = inter.buffer(0)
      
      #x,y = inter.exterior.xy
      #plt.plot(x,y)
  plt.legend(legend)
  plt.savefig(figname + str(layer+1) + ".png")
  plt.close()

