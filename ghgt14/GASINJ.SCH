-- co2 inj

RPTRST
BASIC=5 /
 
WCONPROD 
     'B-3H'      'OPEN'      'LRAT'      3* 50 4* /
     'B-1BH'      'OPEN'      'LRAT'   3* 4000 4* /
      'B-2H'      'OPEN'      'LRAT'    3* 2500 4* /
     'B-4DH'      'OPEN'      'LRAT'     3* 150 4* /
     'D-1CH'      'OPEN'      'LRAT'    3* 300 4* /
     'D-3BH'      'OPEN'      'LRAT'   3* 500 4* /
      'K-3H'      'OPEN'      'LRAT'   3* 100 4* /
      'D-2H'      'OPEN'      'LRAT'   3* 2000 4* /
      'E-1H'      'OPEN'      'LRAT'   3* 6000 4* /
     'E-3CH'      'OPEN'      'LRAT'    3* 800 4* /
     'E-2AH'      'OPEN'      'LRAT'    3* 200 4* /
/
 
WCONINJE 
      'C-1H'       'GAS'  1*      'RATE'  56404.185  1* 600 /
      'C-3H'       'GAS'  1*      'RATE' 1433440.554  1* 600 /
     'C-4AH'       'GAS'  1*      'RATE'   8632.400  1* 600 /
      'F-1H'     'WATER'  1*      'RATE'   9662.379  1* 600 /
      'F-2H'     'WATER'  1*      'RATE'   4574.643  1* 600 /
      'F-3H'     'WATER'  1*    'RATE'  13000.000  1*    450.000 /
/
 
WELOPEN 
     'F-3H'      'SHUT' /
     'K-3H'      'SHUT' /
/
 
WSOLVENT
 C-3H     0.0     /
 C-1H     0.0     /
 C-4AH     0.0     /
/

TUNING
 1 10  0.1  0.15  3  0.3  0.3  1.20  / 
 1* 0.01 1e-5 1e-4 0.1   1e-5  0.02  0.02  / 
 2* 40 1* 15 / 
/

TSTEP
 500*5 /
/
