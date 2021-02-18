#!/usr/bin/env python
import numpy as np
from ecl.eclfile import EclFile
from ecl.grid import EclGrid
from layers import layers

# Script that generates input data to ERT for the layer permeability

# Caprock porosity	fcap	%	35	34-36	Springer and Lindgren (2006)
# Utsira porosity	ffmn	%	36	27-40	Lothe and Zweigel (1999); Holloway et al. (2000)
# Shale porosity	fsh	%	34	31-38	Zweigel et al. (2000); Yang and Aplin (2004). Porosity in shales is very uncertain and controlled by clay content and effective stress.
# Caprock permeability	kcap	mD	0.001	0.00075 - 0.0015	Springer and Lindgren (2006)
# Utsira permeability	kxy	mD	2000	1100 - 5000	Lindeberg et al. (2000)
# Shale permeability	ksh	mD	0.001	0.00075 - 0.0015	Springer and Lindgren (2006). Assume same as caprock, but has a large uncertainty.

fn = "permx.tmpl"
fn2 = "permx.txt"
DISTR = "LOGNORMAL"
permUtsira = np.log(2000)
permvarUtsira = 0.4
permMinMaxUtsira = [1100, 5000]
permShale = np.log(0.001)
permvarShale = 0.4
permMinMaxShale = [0.00075, 0.0015]
dimx = 64
dimy = 118
dimz = 263

keys = ["PERMX"] #,"PORO"]
layerShale, layerUtsira, mapShale, mapUtsira = layers()
numLayers = len(layerShale)
f = open(fn, "w")
f2 = open(fn2, "w") 
for key in keys:
  for layer in range(numLayers):
    f.write("EQUALS \n")
    f.write("'" + key + "'")
    f.write(" <UTSIRA" + key + str(layer+1) + ">")
    f.write(" 1 " + str(dimx) + " 1 " + str(dimy) + " ") 
    f.write(str(layerShale[layer]+1) + " " + str(layerUtsira[layer])) 
    f.write("/\n/\n\n")
    
    f2.write("UTSIRA" + key + str(layer+1) + " " + DISTR + " " + str(permUtsira) + " " + str(permvarUtsira) + "\n")

for key in keys:
  for layer in range(numLayers):
    f.write("EQUALS \n")
    f.write("'" + key + "'")
    f.write(" <SHALE" + key + str(layer+1) + ">")
    f.write(" 1 " + str(dimx) + " 1 " + str(dimy) + " ")
    if layer == 0:
      f.write(str(1) + " " + str(layerShale[layer])) 
    else: 
     f.write(str(layerUtsira[layer-1]+1) + " " + str(layerShale[layer])) 
    f.write("/\n/\n\n")
    f2.write("SHALE" + key + str(layer+1) + " " + DISTR + " " + str(permShale) + " " + str(permvarShale) + "\n")
 
f.close()
f2.close()