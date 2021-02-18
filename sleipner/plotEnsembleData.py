#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

path = "output/simulations/runpath/"

filename = "FEADERS.INC"
figname = "ensembleFeaders"
permstr = "PERMZ"
numLayers = 10

if False:
  filename = "PERMX.INC"
  figname = "ensemblePermLayers"
  permstr = "PERMX"
  numLayers = 18

numEnsembles = 50
numIter = 1

iters = []

layerData = [[] for i in range(numLayers)]
for layer in range(numLayers):
  layerData[layer] = [np.zeros(numEnsembles) for i in range(numIter)]

for iter in range(numIter):
  for ensemble in range(numEnsembles):
    file = open(path + "realisation-"+str(ensemble)+"/iter-"+str(iter)+"/"+filename, 'r') 
    lines = file.readlines()
    layer = 0
    for line in lines:
      if (line.find(permstr)>0):
        perm = line.split()[1]
        layerData[layer][iter][ensemble] = np.log10(float(perm))
        layer = layer + 1        
        


for layer in range(numLayers):
  plt.boxplot(layerData[layer])
  #print(obsDatas)   
  #plt.plot(iters, obsData[layer,0]*np.ones((numIter)),'*')
  plt.savefig(figname + str(layer+1) + ".png")
  plt.close()
