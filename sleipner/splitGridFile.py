#!/usr/bin/env python
fn_orig = 'Sleipner_Reference_Model.grdecl'
fn_cleaned = 'Sleipner_Reference_Model_cleaned.grdecl'
fn_porosity = 'PORO.INC'
f = open(fn_cleaned, "w")
split = open(fn_orig,'r').read().split('REGIONS')
f.write(split[0])
f.close()

g = open(fn_porosity,"w")
g.write(split[1].split('/')[1])
g.write('/\n')
g.close()





