#!/usr/bin/env python
import sys
from operator import itemgetter
from ecl.ecl.ecl_file import EclFile
from ecl.ecl import EclSum
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def collect(l, index):
    return map(itemgetter(index),l)

if __name__ == "__main__":
   
    summary_key = 'FNPR'
    wellname = 'B-1BH'
    summary_input = summary_key #  + ':' + wellname
    
    casekeys = [ ' ', '_CO2', '_GAS']
    namekeys = [ ' ', 'CO2 injection', 'GAS injection']
    pathdirs = ['/history/', '/prediction/', '/prediction/']
    total = [0] * 3
    total_diff = []
    for k in range(3):
        total[k] = [0] * 100

    for j in range(0,3):
    	casekey = casekeys[j]
    	pathdir = pathdirs[j]    	
    	filename = wellname + '_' + summary_key + casekey + '.png'
    	fig = plt.figure(j)
    	for i in range(1,101):
    	    path = "Sim" + str(i) 
            path = path + pathdir
    	    case = path + "ENKF_" + str(i) + casekey
    	    try:
    	        summary = EclSum("%s.SMSPEC" % case)
    	    except:
    	        print ("Issue with the case " + case)
		continue

    	    for key in summary.keys(summary_input):
    	        data = summary[key]
                total[j][i-1] = data.values[len(data) - 1]  - data.values[0]
	        #plt.plot(data.days/365 - data.days[0]/365, data.values/1000, color='blue')
                plt.plot(data.days/365 - data.days[0]/365, (data.values - data.values[0])/1e6, color='blue')
       		#plt.plot( index, p , label="Region:%s  P%d" % (key, index + 1))
    

        plt.ylabel(summary_key + ' [m*sm3]', fontsize=18)
	#plt.ylabel(summary_key + ' [k*sm3/day]', fontsize=18)
        plt.xlabel('Time [years]', fontsize=18)
        plt.title(namekeys[j], fontsize=18)
	#plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))
        #plt.show()
        plt.savefig(filename)
    
    list_of_not_finished_simulations = [94] #[7, 8, 9, 45, 67, 76, 81, 85, 91, 92, 94]
    #list_simulations_with_issues = [4, 5, 30, 31, 32, 33, 34, 34, 35, 41, 49,50,51,52, 95,96,97,98,99,100]
    for k in range(100):
        if not k+1 in list_of_not_finished_simulations : #and not k+1 in list_simulations_with_issues :
            total_diff.append ( (total[1][k] - total[2][k]) / 1e6)

    #print total
    #print total_diff
    plt.figure(3)
    plt.hist(total_diff)
    plt.ylabel('Number of ensembles', fontsize=18)
    plt.xlabel('FOPT' + ' [m*sm3]', fontsize=18)
    plt.title('Increase in total oil production compared to pure gas injection', fontsize=14)
    #plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))
    plt.savefig('histogram_enhanced_FOPT.png')
    
        


