#!/usr/bin/env python
import sys
from operator import itemgetter
from ecl.ecl.ecl_file import EclFile
from ecl.ecl import EclSum
import matplotlib.pyplot as plt
import numpy as np

def collect(l, index):
    return map(itemgetter(index),l)

if __name__ == "__main__":
    total_times=[]
    for i in range(1,101):
    	#path = "Sim" + str(i) + "/"  + "history/"
	path = "Sim" + str(i) + "/prediction/"	
    	case = path + "ENKF_" + str(i)
        case = case + "_CO2"
    	try:
    	    prt = open("%s.PRT" % case)
    	except:
    	    print ("Issue with PRT file of case " + case)
            continue

        finished=False
        for line in prt:
            if "Total time (seconds):" in line:         
                for number in line.split():
	            try:
                        fl = float(number)
                        if fl > 300 and fl < 5000: # Exlude total time over 5000s from the histogram
                        	total_times.append(float(number))
                        else:
                             print ("Issue with case " + case + " Run time " + str(fl))
                        break
		    except:
                        a = number

		finished=True
                break
                        
 	if not finished:
            print ("Simulation did not finish for case " + case)

    print ("Mean time " + str(np.mean(total_times)))
    print ("Max time " + str(np.max(total_times)))
    print ("Min time " + str(np.min(total_times)))
    print(total_times)
    plt.figure(1)
    plt.hist(total_times)
    plt.xlabel('Simulation time' + ' [s]', fontsize=18)
    plt.ylabel('Number of ensembles', fontsize=18) 
    #plt.title('Total simulation time', fontsize=14)
    plt.savefig("simulationTimesCO2_mod")
    #plt.show()

    
	    

        

        
        
