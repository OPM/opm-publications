
Title: Open Reservoir Simulator for CO2 Storage and CO2-EOR
Authors: Tor Harald Sandve (IRIS), Atgeirr F. Rasmussen (Sintef) and Alf Birger Rustad (Equinor) 
Presented at: 14th International Conference on Greenhouse Gas Control Technologies, GHGT-14, 21-25 October 2018, Melbourne Australia

OPM-version: 04-2018 Release

In order to run the case you first need to download the norne model from https://github.com/OPM/opm-data/tree/master/Norne/
Code to generate multiple realizations of the Norne model can be downloaded from https://github.com/rolfil/Norne-Initial-Ensemble
The results in the paper is based on history matched parameters, the history matching
code used for this is unfortunately not available. 

Data files is made available under the Open Database
License: http://opendatacommons.org/licenses/odbl/1.0/. Any rights in
individual contents of the database are licensed under the Database Contents
License: http://opendatacommons.org/licenses/dbcl/1.0/
While programs and scripts are distributed under the GNU General Public License, version 3 or later (GPLv3+).
The authors holds copyright to all contents. 

## Content: 

# Copy these files to the INCLUDE directory in the Norne model 
# They add solvent related keywords with CO2 properties to the deck
CO2INJ.SCH 
co2_misc.inc
co2_prop_mod.inc
GASINJ.SCH

# python scripts to handle ensemble of models. 
# probably need some hand tuning to make it work for your case 
distToddLong.py 
modifyDataFile.py
plotEnsambles.py
runtimeEnsambles.py



