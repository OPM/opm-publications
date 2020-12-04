#!/usr/bin/env python
import os;

base="SPE5CASE"
cases=["1", "2", "3"]
models=["DYN", "FIXED", "SOLVENT"]
flow = "~/workspace/opm/opm-simulators/build/bin/flow "
dir="results"
output = " --output-dir="+dir +" --enable-opm-rst-file=true --tolerance-mb=0.8e-6"
for case in cases:
 for model in models:
   name = base + case + "_" + model
   os.system(flow + name + output)