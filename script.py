from pathlib import Path
from itertools import product
import numpy as np
import subprocess
import os

# vals and ranges 

def decimal_range(start, stop, step):
    values = []
    value = start 

    while value <= stop:
        values.append(round(value,10))
        value += step 

    return values

E1_values = range(100, 300, 50)
E2_values = decimal_range(0.01, 0.02, 0.005)
E3_values = range(10, 50, 10)


# output folder 
output_dir = Path("/Users/namiraferozachowdhury/Desktop/N8CIR_internship/output")

# loop for the files to be generated 

for i, (E1, E2, E3) in enumerate(
   zip(E1_values, E2_values, E3_values)
):
  
    filename = os.path.join(
        output_dir,
        f"example_{i}.py"
    )
    with open(filename, 'w') as file:

        file.write(

        f"""
import sys
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

#DEFINE vals variables # lg added
E1={E1}
E2={E2}
E3={E3}

# stop jnl file from using getSequenceFromMask
session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

mdb.ModelFromInputFile(inputFileName=
    '/scratch//bs232nc/n8-internship/ax1_comp_2_original.inp', name='cyl')
Mod = mdb.models['cyl']

del mdb.models['Model-1']

# Material elastic table values
#   E1 E2 E3 nu12 nu13 nu23 G12 G13 G23

#vals = [100.0, 250.0, 200.0, 0.01, 0.01, 0.01, 99.0099, 13.0, 13.0] # lg commented out
vals = [E1, E2, E3] # lg added in

Mod.materials['IVDAF'].elastic.setValues(table=(tuple(vals), ))

jobName = "jobtest"
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF,
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF,
    memory=90, memoryUnits=PERCENTAGE, model=Mod, modelPrint=
    OFF, name=jobName, nodalOutputPrecision=SINGLE, numCpus=1, numGPUs=0,
mdb.saveAs('edited_model.cae')

# Optionally submit automatically
mdb.jobs[jobName].submit(consistencyChecking=OFF)
# Or to create an INP file, uncomment the following instead.
# mdb.writeFile(example.inp)


         """)

    print(
        f"example_{i}.py"
        f"E1={E1}"
        f"E2={E2}"
        f"E3={E3}"
    )




# confirmation for where the files are 

print(f"Files saved to: {output_dir.resolve()}")
subprocess.run(["open", str(output_dir.resolve())])