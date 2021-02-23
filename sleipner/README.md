# Sleipner history matching

This folder contains the necessary input for reproducing the history matching as presented at 
the IEAGHG Webinar Sleipner Benchmark study, 25th February 2021.
The three type of parameters we tried to match was the feeder permeability, the layer permeability and the temperature on the top. The history matching is done using ERT and the Flow simulator.

Data files in this folder is made available under the Open Database
License: http://opendatacommons.org/licenses/odbl/1.0/. Any rights in
individual contents of the database are licensed under the Database Contents
License: http://opendatacommons.org/licenses/dbcl/1.0/
While programs and scripts are distributed under the GNU General Public License, version 3 or later (GPLv3+).
The authors holds copyright to all contents. 

Note that other licenses may apply to files and programs downloaded during the setup of the history matching

## Installation
To run the history matching you will first need to install
* Flow (https://opm-project.org)
* ERT (https://github.com/equinor/ert)

You will also need to install some python packages see ```requirements.txt``` for a complete list 

You can install all the required python packages including ERT in a virtual environment with the following commands:

```bash
# Create virtual environment
python -m venv .venv
# Activate virtual environment
source .venv/bin/activate
pip install -r requirements.txt
```

You can install Flow from binary packages on Ubuntu Linux 16.04 or 18.04 and Red Hat Enterprise Linux 6 or 7
Installing instruction is found here: https://opm-project.org/?page_id=245
The opm webpage also has instruction for instalation on other systems. 

## Download the following files from Sleipner benchmark
(https://co2datashare.org/dataset/sleipner-2019-benchmark-model)
* Sleipner_Reference_Model.grdecl ("Sleipner Reference Model 2019 Grid")
* Feeder data ("Feeders")
* Sleipner plume boundaries ("Sleipner plume boundaries")

You can select the three items and press "Download selected". Unzip the ```download.zip``` file, and all the included ```.zip``` files,  in the current ```sleipner``` directory,
Move the following files/directories to the current folder
* ```Sleipner_Reference_Model_2019_Grid/data/Sleipner_Reference_Model.grdecl``` 
* ```feeders/data/Main_feeder_chimney```
* ```feeders/data/NE_feeder_L5_L6_low_confidence```
* ```feeders/data/SW_feeder_L7_L8_low_confidence```
* ```sleipner_plumes_boundaries/Sleipner_Plumes_Boundaries``` 

## Splitting the grid file
The grid file needs to be split before usage:

```bash
python splitGridFile.py
```

## Setting up the history matching
For the history matching we use the build-in functionality in ERT to represent the uncertainty in the parameters.
The permeabilities is assumed to have a lognormal distribution with

  X  | utsira    | shale       | feeders
  -- | --------- | --------- |  --------
 mean| log(2000) | (log(0.001) | log(1)
 std | 0.4       | 0.4         | log(100)

The scripts **feeder.py** and **layerPermeability.py**
is used to set up the input permeabilities for the ERT. Simply run them as follows

```bash
python feeder.py
python layerPermeability.py
```

These scripts will create
*feeders.tmpl*, *feeders.txt*, *permx.tmpl* and *permx.txt*
that are used to configure ERT.

The top temperature we use a normal distribution with mean 34C and standard deviation 3C
and specified in
*rtempvd.tmpl* and *rtempvd.txt*

The history matching uses the CO2 plume contour areas in the layers. To compute the observed areas the script
**obs_area.py**
needs to be run:

```bash
python obs_area.py
```

This will generate a ```plume_obs_data.txt``` file with the areas computed from the polygons with 10% uncertainty in data.

The final setup step is to setup the ERT file
The
**sleipner.ert**
file is a good starting point but needs to be adjusted with your own paths and configuration. Look for "replace_with_absolute_path" in the file. You can also adjust the number of ensemble members in this file. For debugging, it is probably a good idea to reduce the number of ensemble members to get a faster runtime (but lower accuracy, of course).

## Running the history matching

To run the history matching you now simply type

`ert ensemble_experiment sleipner.ert`

for a dry run without any update. Or

`ert sleipner.ert es-mda`

to run with the es-mda method.

See *ert --h* and the ERT manual for how to configure ERT and use other history-matching methods and setup


## Running on a cluster

In order to run the ensemble on a cluster, you will need to modify the file sleipner.ert and specify the correct QUEUE_SYSTEM variable to either SLURM or LSF. Consult the ERT documentation for specific information for each queuing system.
