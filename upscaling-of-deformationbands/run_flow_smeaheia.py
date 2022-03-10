from joblib import Parallel, delayed
import time
import os
from matplotlib import pyplot as plt
from opm.io.ecl import ESmry


def copyCase(ind, case, ending1, ending2, ending3, ending4):
  #COPY FILE
  fn1 = "vette" + ending1
  fn12 = "vette_" + str(ind) + ending1
  fn2 = "vette" + ending2
  fn22 = "vette_" + str(ind) + ending2
  
  fn3 = "vette" + ending3
  fn32 = "vette_" + str(ind) + ending3
  fn4 = "vette" + ending4
  fn42 = "vette_" + str(ind) + ending4
  
  fn5 = "GRID.INC"
  fn52 = "../GRID.INC"
  
  file = open(case + ".DATA", "r")
  replacement = ""
  # using the for loop
  for line in file:
    line = line.strip()
    line = line.replace(fn1, fn12)
    line = line.replace(fn2, fn22)
    line = line.replace(fn3, fn32)
    line = line.replace(fn4, fn42)
    line = line.replace(fn5, fn52)

    replacement = replacement + line + "\n"

  file.close()
  # opening the file in write mode
  fout = open("input/" + case + "_"+ str(ind)+ ".DATA", "w")
  fout.write(replacement)
  fout.close()
  
def flow(samp_ind, K1, K2, kfakm):
    time.sleep(1)
    os.system("python3 vetteDeformMultx.py " + str(samp_ind) + " " + str(kfakm))
    os.system("python3 vetteAquifer.py " + str(samp_ind) + " " + str(K1) + " " + str(K2))
    casename = "SMEAHEIA_" + str(samp_ind)
    copyCase(samp_ind, "SMEAHEIA", ".aqunum", ".aqucon", ".multx", ".multy")
    flowpath = "~/workspace/opm/opm-simulators/build/bin/flow"
    os.system("mpirun -np 1 " + flowpath + " input/" + casename + ".DATA --output-dir=output > " + "output/" + casename + ".out")
    
def anqr(samp_ind):
    casename = "output/SMEAHEIA_" + str(samp_ind)
    smry = ESmry(casename + ".SMSPEC")
    anqr1 = smry["ANQR:1"]
    anqr2 = smry["ANQR:1"]
    return [anqr1[-1],anqr2[-1]]

def anqp(samp_ind):
    casename = "output/SMEAHEIA_" + str(samp_ind)
    smry = ESmry(casename + ".SMSPEC")
    anqr1 = smry["ANQP:1"]
    anqr2 = smry["ANQP:1"]
    return [anqr1[-1], anqr2[-1]]

def plotter(caseid, pickcase, pickval, data, ylabel, figname, cases, kfakms):
  legendstr = []
  plt.figure(1)
  for kfakm in kfakms:
    tmp = []
    tmp2 = [] 
    for val, case in zip(data, cases):
      if (case[pickcase] == pickval and case[3] == kfakm):
        tmp.append(-val[caseid])
        tmp2.append(case[caseid+1]*40/500) # plot vs transmissibility
        
    print(tmp2, tmp)
    plt.plot(tmp2, tmp)
    if (kfakm > 10000):
      legendstr.append("BASE" + " [m$^{-1}$]")
    else:
      legendstr.append(str(kfakm) + " [m$^{-1}$]")

  plt.legend(legendstr)
  plt.xlabel("Transmissibility [m X mD]")
  plt.xscale('log')
  plt.ylabel(ylabel)
  plt.savefig(figname + ".png")
  plt.close()

# Run a set of simulations with these parameters
k1s = [1,1e1,1e2,1e3,1e4, 1e5, 1e6]
k2s = []
kfakms = [1e-2, 1e-1, 1, 1e1, 1e9]

ids = []
cases = [] 
ind = 0
for k2 in k2s:
  k1 = 1e-2
  for kfakm in kfakms:
    cases.append([ind, k1, k2, kfakm])
    ids.append(ind)
    ind = ind + 1
for k1 in k1s:
  k2 = 1e-5
  for kfakm in kfakms:
    cases.append([ind, k1, k2, kfakm])
    ids.append(ind)
    ind = ind + 1

# Run the simulations in parallel
Parallel(n_jobs=2)(delayed(flow)(ind, k1, k2, kfakm) for ind, k1, k2, kfakm in cases)

# Plot aqufifer pressure and rates
anqrs = []
anqps = []
for ind in ids:
  anqrs.append(anqr(int(ind)))
  anqps.append(anqp(int(ind)))

plotter(0, 2, 1e-5, anqrs, "Outflux rate [SM3/day]",  "anqrs", cases, kfakms)
plotter(0, 2, 1e-5, anqps, "Aquifer pressure [Barsa]", "anqps", cases, kfakms)

