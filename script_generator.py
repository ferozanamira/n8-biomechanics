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
#mdb.jobs[jobName].submit(consistencyChecking=OFF)
# Or to create an INP file, uncomment the following instead.
# mdb.writeFile(example.inp)

#-----------------------------------------------------------------------------
# NEW BITS
#=----------------------------------------------------------------------------

step_name = 'Step-1'           # Replace with the name of your step
applied_disp = -2.5            # Applied displacement in U3 (mm)

# Optionally submit automatically
my_job = mdb.jobs[jobName]
my_job.submit(consistencyChecking=OFF)

# This is the command that pauses Python execution until the Abaqus solver finishes
my_job.waitForCompletion()
print('Job %s completed successfully.' % jobName)

# 2. OPEN THE RESULTING ODB FILE
odb_path = jobName + '.odb'
odb = openOdb(path=odb_path)

#  EXTRACT REACTION FORCE
# Access the last frame of the specified step to get the final reaction force
last_frame = odb.steps[step_name].frames[-1]

# Get the entire Reaction Force (RF) field output for that frame
rf_field = last_frame.fieldOutputs['RF']

# Locate the node set called 'TOP'. 
# NOTE: This assumes 'TOP' was created at the Assembly level. 
# If you created it on the part instance, you will need to change this line to:
# top_set = odb.rootAssembly.instances['YOUR_INSTANCE_NAME'].nodeSets['TOP']
top_set = odb.rootAssembly.nodeSets['TOP']

# Filter the overall reaction force field down to just the nodes in the 'TOP' set
rf_at_top = rf_field.getSubset(region=top_set)

# Sum the reaction forces in the 3rd direction (U3 / Z-axis)
# The .data attribute contains an array of [RF1, RF2, RF3]. Index 2 is RF3.
total_rf3 = 0.0
for node_value in rf_at_top.values:
    total_rf3 += node_value.data[2]

# 4. CALCULATE STIFFNESS
# Stiffness K = Force / Displacement
# We use absolute values to get a standard positive stiffness magnitude
stiffness = abs(total_rf3) / abs(applied_disp)

# 5. OUTPUT RESULTS TO THE MESSAGE AREA / COMMAND LINE
print('--- RESULTS ---')
print('Total Reaction Force (RF3) at TOP: %.4f' % total_rf3)
print('Applied Displacement (U3): %.4f mm' % applied_disp)
print('Calculated Stiffness: %.4f (Force units / mm)' % stiffness)
print('---------------')

# addition change to print ti file rather than print (not sure where the print statements actually go)
filename="out1.txt"
with open(filename, w) as f:
        f.write(stiffness)


# Close the ODB to free up memory and remove the file lock
odb.close()

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