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

# stop jnl file from using getSequenceFromMask
session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

mdb.ModelFromInputFile(inputFileName=
    'ax1_comp_2.inp', name='cyl')
Mod = mdb.models['cyl']

del mdb.models['Model-1']

# Material elastic table values
#   E1 E2 E3 nu12 nu13 nu23 G12 G13 G23 

vals = [100.0, 250.0, 200.0, 0.01, 0.01, 0.01, 99.0099, 13.0, 13.0]


Mod.materials['IVDAF'].elastic.setValues(table=(tuple(vals), ))

jobName = "jobtest"
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model=Mod, modelPrint=
    OFF, name=jobName, nodalOutputPrecision=SINGLE, numCpus=1, numGPUs=0, 
    queue=None, resultsFormat=ODB, scratch='', type=ANALYSIS, userSubroutine=''
    , waitHours=0, waitMinutes=0)

mdb.saveAs('edited_model.cae')

# Optionally submit automatically
# mdb.jobs[jobName].submit(consistencyChecking=OFF)
# Or to create an INP file, uncomment the following instead.
# mdb.writeFile(example.inp)

