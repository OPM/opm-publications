Instruction on how to reproduce field-scale simulation results using the Smeaheia Dataset for
the paper **"Impact of deformation bands on fault-related fluid flow in field-scale simulations."**

## The Smeaheia Dataset
The Smeaheia Dataset has been published by Gassnova SF and Equinor ASA
and is available from

   https://co2datashare.org/dataset/smeaheia-dataset

We recommend visiting that site for full information about the data set,
as well as more data than that provided here, which is only a simulation
model.

The data in this directory are owned by Equinor ASA and Gassnova SF

The license of the data is the SMEAHEIA DATASETS LICENSE
which can be found in the 'SMEAHEIA%20DATASET%20LICENSE_Gassnova%20and%20Equinor.pdf' file, as well as at:

   https://co2datashare.org/smeaheia-dataset/static/SMEAHEIA%20DATASET%20LICENSE_Gassnova%20and%20Equinor.pdf

A summary of the license is available here:

   https://co2datashare.org/view/license/26af9426-203f-4993-9d41-2e1bf191ceaf

## Installation
The following python packages are needed:
* joblib
* time
* sys
* matplotlib
* numpy
* opm
* scipy
* os


We recommend installing in virtual environment using pip
```bash
# Create virtual environment
python -m venv .venv
# Activate virtual environment
source .venv/bin/activate
# installing joblib
pip install joblib
# installing opm including the simulator Flow
pip install opm
# etc.
```
For newer versions of flow see https://opm-project.org.

## Run the simulations
1. Unzip ```GRID.ZIP``` to ```GRID.INC``` and ```SMEAHEIA_EGRID.ZIP``` to ```SMEAHEIA.EGRID```
2. Create directory ```input``` and ```output```
3. Set flow install path in ```run_flow_smeaheia.py``` and adjust parallel setup in the run script
4. Run ```run_flow_smeaheia.py```

Note that the script takes some time to run due to slow and unoptimized  upscaling routines in
```analytical_effective_perm.py```. 

## List of files
* ```run_flow_smeaheia.py ``` script to run the simulations
* ```analytical_effective_perm.py``` code that computes the upscaled effective permeability
* ```utils.py``` utilities used by ```analytical_effective_perm.py```
* ```vetteAquifer.py``` creates the input files for the numerical aquifer
* ```veteDeformMultx.py``` creates the input files for the connection between vette and the aquifer and the permeability multipliers that account for the effect of the deformationbands
* ```SMEAHEIA.DATA``` the simulation model adapted from the Gassnova simulation model shared via CO2SHARE
* ```GRID.ZIP``` the simulation grid extracted from the Gassnova simulation model shared via CO2SHARE
* ```SMEAHEIA_EGRID.ZIP``` A EGRID file that contains the grid. Used by vetteDeformMultx.py
