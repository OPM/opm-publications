#!/usr/bin/env python
import sys
from operator import itemgetter
from ecl.ecl.ecl_file import EclFile
from ecl.ecl import EclSum
import matplotlib.pyplot as plt


def collect(l, index):
    return map(itemgetter(index),l)

if __name__ == "__main__":
    #case = sys.argv[1]
    for i in range(1,101):
    	path = "Sim" + str(i)
    	case = path + "/ENKF_" + str(i)
        caseNew = case + "_CO2"
    	try:
    	    orig = open("%s.DATA" % case)
    	except:
    	    print ("Issue with .data file of case " + case)

	new = open("%s.DATA" % caseNew, 'w+')
        for line in orig:
            if "VAPOIL" in line:
                mod = line + "\n\nSOLVENT \n\nMISCIBLE\n 1  20 / \n"
		new.write(mod) 
            elif "SCALECRS" in line:
                mod = "INCLUDE\n '$ECLINC/co2_misc.inc' / \n\nINCLUDE\n'$ECLINC/co2_prop_mod.inc' /\n\n" + line
                new.write(mod) 
            elif "SOLUTION" in line:
                mod = line + "\n \nRESTART \n 'history/ENKF_" + str(i) + "' 240 / \n"
                new.write(mod)
            elif "'../NORPT_NOKH.SCH' /" in line:
                mod = line + "\n\nINCLUDE\n '$ECLINC/CO2INJ.SCH' / \n\n"
                new.write(mod)         
            else:
                new.write(line)
        	
	    

        

        
        
