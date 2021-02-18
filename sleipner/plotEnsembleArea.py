#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

path = "output18/simulations/runpath/"
filename = "plume_areas_0.out"
filenameData = "plume_obs_data.txt"
figname = "ensembleplot"
numEnsembles = 50
numIter = 5
numLayers = 9

obsData = np.genfromtxt(filenameData,dtype=(float))
obsDatas = []
iters = []

layerData = [[] for i in range(numLayers)]
for layer in range(numLayers):
  layerData[layer] = [np.zeros(numEnsembles) for i in range(numIter)]

for iter in range(numIter):
  for ensemble in range(numEnsembles):
    areas = np.genfromtxt(path + "realisation-"+str(ensemble)+"/iter-"+str(iter)+"/"+filename, dtype=(float))
    for area, layer in zip(areas, range(numLayers)):
      layerData[layer][iter][ensemble] = area
      
  obsDatas.append(obsData[layer,0])
  iters.append(iter+1)

for layer in range(numLayers):
  plt.boxplot(layerData[layer])
  print(obsDatas)   
  plt.plot(iters, obsData[layer,0]*np.ones((numIter)),'*')
  plt.savefig(figname + str(layer+1) + ".png")
  plt.close()
