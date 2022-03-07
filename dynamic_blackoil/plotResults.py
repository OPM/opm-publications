#!/usr/bin/env python
from opm.io.ecl import ESmry, ERst
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from datetime import datetime  
from datetime import timedelta
import numpy as np
base="SPE5CASE"
cases=["1", "2", "3"]
models=["DYN", "FIXED","SOLVENT"] 
modelsName = ["DYNAMIC", "FIXED","STANDARD"]
path=""
dir="results/"
keys=["WOPR", "WGPR", "WWPR", "WOPT", "WGPT", "WWPT"]
titles = ["Oil production rate [Stb/day]", "Gas production rate [MSCF/day]", 
"Water production rate [Stb/day]", "Total oil production [Stb]",
"Total gas production [Stb]", "Total water production [Stb]"]
rstkeys = ["SOIL", "SGAS", "SWAT", "PRESSURE", "RS", "SSOLVENT"]
rstTitle = ["Oil saturation", "Gas saturation", "Water saturation", "Pressure [Psia] ", "Rs [Stb/MSCF]", "Solvent saturation"]
well="PROD"
# pick cell [3,3,1]
cell_idx = (0 * 49) + (2 * 7) + 2

plt.rcParams.update({'axes.titlesize': 'x-large'})
plt.rcParams.update({'axes.labelsize': 'x-large'})
plt.rcParams.update({'xtick.labelsize': 'x-large'})
plt.rcParams.update({'ytick.labelsize': 'x-large'})

for key,title in zip(keys,titles):
  for case in cases:
    legend_str = []
    for model, modelname in zip(models, modelsName):
      name = base + case + "_" + model
      pathtmp = path
      if (model != "E300"):
        pathtmp = path + dir
      
      summary = ESmry("%s%s.SMSPEC" % (pathtmp,name))
      years = summary["YEARS"]
      data = summary[key+":"+well]
      plt.plot(years,data)
      legend_str.append(modelname)
 
    plt.ylabel(title)
    plt.xlabel("years")
    plt.legend(legend_str, loc = 'best')
    plt.savefig(dir + key + case + ".png", bbox_inches='tight')
    plt.close()

for key, title in zip(rstkeys, rstTitle):
  for case in cases:
    legend_str = []
    for model, modelname in zip(models, modelsName):
      name = base + case + "_" + model
      pathtmp = path
      if (model != "E300"):
        pathtmp = path + dir
		
      summary = ESmry("%s%s.SMSPEC" % (pathtmp,name))
      report_time = summary["YEARS", True]
      report_time = np.insert(report_time, 0, 0.0, axis=0)
      restart_file = ERst("%s%s.UNRST" % (pathtmp,name))
      if (key == "SSOLVENT" and model !="SOLVENT"):
        continue
		
      data_rst = []
      remove_idx = []
      for rst in restart_file.report_steps:
        if (key == "SOIL"):
          try:
            sgas = restart_file["SGAS",rst]
            swat = restart_file["SWAT",rst]
            ssol = sgas
            if (model == "SOLVENT"):
              ssol = restart_file["SSOLVENT",rst]
        
            soil = 1.0 - sgas[cell_idx] - swat[cell_idx]
            if (model == "SOLVENT"):
              soil -= ssol[cell_idx] 
          
            data_rst.append(soil)
          except:
            remove_idx.append(rst)

        else:
          try: 
            data = restart_file[key, rst]
            data_rst.append(data[cell_idx])
          except:
            print(name)
            print(rst)
            remove_idx.append(rst)

      report_time = np.delete(report_time,remove_idx,axis=0)

      plt.plot(report_time, data_rst, lw=2)
      legend_str.append(modelname)
	  
    plt.ylabel(title)
    plt.xlabel("years")
    plt.legend(legend_str, loc = 'best')
    plt.savefig(dir + key + case + ".png", bbox_inches='tight')
    plt.close()