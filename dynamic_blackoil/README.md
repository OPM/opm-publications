# Data-set for the simulations in the paper:
Sandve, T.H., Sævareid, O. & Aavatsmark, I. Dynamic PVT model for CO2-EOR black-oil simulations. Comput Geosci (2022). https://doi.org/10.1007/s10596-022-10133-x

To run the cases you will need Flow version 04.2021 or later.
(or the current master version) 

## Main input decks for case 1-3
- CASE 1: pressure below MMP
- CASE 2: pressure above MMP
- CASE 3: pressure first below MMP and than above MMP

### The standard solvent model
- SPE5CASE[1-3]_SOLVENT.DATA
- SPE5.BASE

### The fixed fraction PVT model
- SPE5CASE[1-3]_FIXED.DATA
- SPE5_FIXED.BASE
- PVTSOL_HYBRID_A00_A02.pvt

### The dynamic fraction PVT model
- SPE5CASE[1-3]_DYN.DATA
- SPE5_DYN.BASE
- PVTSOL_HYBRID_ST00_ST02.pvt

### The composisional PVT model
- SPE5CASE[1-3]_SOLVENT.DATA
- SPE5e300PVT

### Common base files
- SPE5_GRID.BASE
- SPE5_RELPERM.BASE
- SPE5_SUMMARY.BASE 
- SPE5CASE[1-3]_WELL.BASE 
- SPE5CASE[1-3].SCH

## Script for running and plotting
- runSPE5.py 
- plotResults.py 

Note: paths needs to be modified to align with your instalation. 
