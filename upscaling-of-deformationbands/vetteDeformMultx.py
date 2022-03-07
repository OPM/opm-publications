#!/usr/bin/env python
import numpy as np
from analytical_effective_perm import damage_zone_width
from analytical_effective_perm import damage_zone_permeability
from analytical_effective_perm import damage_zone_width_full
from opm.io.ecl import EGrid
import sys

def isvette(xyz):
  return xyz[1][0]>6667544.54 and xyz[1][0]<6761381.72 and xyz[0][0]>550000 and xyz[0][0]<561000 

def throw(y):
  maxPoint = 6739819.56
  minPoint = 6667544.54
  return 500 * (1.0 - (abs(maxPoint - y) / (maxPoint - minPoint)) )

# Read case number and effective permeability ratio (kfakm)
ind = ""
if(len(sys.argv) > 1):
    ind = str(sys.argv[1])

kfakm = 0.1
if(len(sys.argv) > 2):
    kfakm = float(sys.argv[2])


# Set and read grid file     
casename ="SMEAHEIA.EGRID"
grid = EGrid(casename)

# Apply effect of deformation bands
deform = True;

# Location of input files for the simulations
fn3 = "input/vette_"+ ind + ".aqucon"
fn4 = "input/vette_"+ ind + ".multx"
fn5 = "input/vette_"+ ind + ".multy"

# Read fault data
boundaryfile = "Fault.grdecl"
boundarytxt = np.genfromtxt(boundaryfile, skip_header=2, skip_footer=1, dtype=("|U10", int, int, int, int, int, int, "|U1", "|U1"))

ijks = []
ijks_bot = []
directions = []
for txt in boundarytxt:
  if ([txt[1]-1,txt[3]-1,txt[5]-1] in ijks) and ([txt[2]-1,txt[4]-1,txt[6]-1] in ijks_bot):
    continue
    
  ijks.append( [int(txt[1]-1),int(txt[3]-1),int(txt[5]-1)])
  ijks_bot.append( [txt[2]-1,txt[4]-1,txt[6]-1])
  directions.append(str(txt[7]))


# Write AQUCON, MULTX and MULTY
h = open(fn3, "w")
h.write("AQUCON\n")
g = open(fn4, "w")
f = open(fn5, "w")

connum = 0
yloc = []
heigth = []
for ijk, ijk_bot, direction in zip(ijks, ijks_bot,directions):
  xyz = grid.xyz_from_ijk(ijk[0], ijk[1], ijk[2])
  if (isvette(xyz)):
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]
    t = throw( xyz[1][0])
    perms = damage_zone_permeability(t, None,kfakm)
    transMult = 1.0
    dl = damage_zone_width_full(t)
    X = dl / 200;
    if (deform):
      transMult = perms[0] / (perms[0] * (1.0 - X) + X)
      
    yloc.append(xyz[1][0])
    heigth.append(t)
    for aqunum in range(1,2):
      if (direction == "J" and aqunum == 1):
        f.write("BOX\n")
      elif (direction == "I" and aqunum == 1):
        g.write("BOX\n")
      colnum = 0
      h.write(str(aqunum) + " ")

      for top,bot,ind in zip(ijk,ijk_bot,range(3)):
        top_mod = top + 1
        bot_mod = bot + 1
        if (direction == "I"  and ind == 0):
          top_mod = top_mod + 1
          bot_mod = bot_mod + 1
        
        if (direction == "J" and ind == 1):
          top_mod = top_mod + 1
          bot_mod = bot_mod + 1
        if (ind == 2):
          colnum = bot - top      
        h.write(str(top_mod) + " " + str(bot_mod) + " ")
        if (direction == "J" and aqunum == 1):
          f.write(str(top_mod) + " " + str(bot_mod) + " ")
        elif (direction == "I" and aqunum == 1):
          g.write(str(top_mod) + " " + str(bot_mod) + " ")
      
      if (direction == "J" and aqunum == 1):
        f.write("/\n\nMULTY- \n "+str(colnum+1)+"*" + str(transMult) + "/\n\n")
      elif (direction == "I" and aqunum == 1):
        g.write("/\n\nMULTX- \n "+str(colnum+1)+"*" + str(transMult) + "/\n\n")

      if (aqunum == 1):
        h.write("'" +direction + "-' " + str(1.0) + " 0/\n")
      elif (aqunum == 2):
        h.write("'" +direction + "-' " + str(1.0) + " 1/\n")

      if (direction == "J" and aqunum == 1):
        f.write("ENDBOX\n\n")
      elif (direction == "I" and aqunum == 1):
        g.write("ENDBOX\n\n")
      connum =connum + 1

h.write("/\n")
h.close()
g.close()
f.close()


# write vette height 
y1 = 1e99
y2 = 0
y3 = 0
h1 = 0
h2 = 0
h3 = 0
for y, h in zip(yloc, heigth):
  if y < y1:
    y1 = y
    h1 = h
  if y > y3:
    y3 = y
    h3 = h
  if h > h2:
    h2 = h
    y2 = y

yloc2 = [y1, y2, y3]
hloc2 = [h1, h2, h3]
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (20,2)
plt.plot(yloc2, hloc2)
plt.ylabel('height')
plt.xlabel('y-cooridinates', )
plt.savefig('vetteHeight.png')
