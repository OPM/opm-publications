
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

The following files needs to be copied to the INCLUDE directory in the Norne model. They add solvent related keywords with CO2 properties to the deck.

Note that in OPM Flow SWOF and SGOF can be combined with SOF2. I.e. no need to convert them into SWFN, SGFN and SOF3. 

* CO2INJ.SCH 
* co2_misc.inc
* co2_prop_mod.inc
* GASINJ.SCH

The folder also includes some python scripts to run the ensembles. 
They are uploaded as is and will need some hand to make it work on your system. 

* distToddLong.py 
* modifyDataFile.py
* plotEnsambles.py
* runtimeEnsambles.py



