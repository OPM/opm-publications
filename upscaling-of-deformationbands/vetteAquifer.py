#!/usr/bin/env python
import sys

ind = ""
if(len(sys.argv) > 1):
    ind = str(sys.argv[1])

K1 = 1
if(len(sys.argv) > 2):
    K1 = sys.argv[2]

K2 = 1
if(len(sys.argv) > 3):
    K2 = sys.argv[3]

fn = "input/vette_" + ind + ".aqunum"
h2 = open(fn, "w")
h2.write("AQUNUM\n")
h2.write("-- id  I J K Area Length Poro K Depth Initial Pr PVTNUM SATNUM \n")
h2.write("1 1 1 1 40 500 1e12 " + K1 + " 1* 1* 1 1 /\n") # t = 10 / 400 rate = 0.015 kg /s 
#h2.write("1 1 1 1 40 1000 1e12 " + K1 + " 1000 1 1 1 /\n") # t = 10 / 400 rate = 0.015 kg /s 

#h2.write("1 1 1 1 20 1000 1e10 " + K1 + " 500 50 1 1 /\n") # t = 10 / 400 rate = 0.015 kg /s
#h2.write("2 1 1 6 4e3 0.1 1e12 " + K2 + " 1* 1* 1 1 /\n") # t = 1
#h2.write("1 1 1 1 0.1 1000 1e7 " + K1 + " 500 50 1 1 /\n") # t = 10 / 400 rate = 0.015 kg /s
#h2.write("2 1 1 6 1e5 1e3 0.3 " + K2 + " 1* 1* 1 1 /\n") # t = 1
h2.write("/\n")
h2.close()

