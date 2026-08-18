# n8-biomechanics

**Workflow has 2 steps:**
1. Generate Python scripts.
2. Run Abaqus job on Air (as a job array).


## 1. Generate Python scripts.
2 scripts 
1. `script_generator.py` - this is the template for generating the Python scripts, includes a decimal range loop to provide different values to material properties values. This scripts generates python scripts with the naming convention `example_<num>.py`.
2. `generator.sh` - this is the submission script to run `script_generator.py` on Aire.


## Run Abaqus job on Air (as a job array). 
1 script 
1. `abaqusjobarray.sh` - This is the submission script that runs an Abaqus job using the `example_<num>.py` files. Each `example_<num>.py` runs as a different job array running abaqus each time.

## Set-up 

1. Clone the repo on Aire (HTTPS)

navigate into n8-biomechanics
```
cd n8-biomechanics
```

1. Change `script_generator.py` directory paths 

a. out directory change line 25
```
output_dir = Path("your/path/to/n8-biomechanics/")
```

b. path to the input file on Aire line 65
```
mdb.ModelFromInputFile(inputFileName=
    'your/path/to/file.inp', name='cyl')
```

## Running workflow 
1. Run generator script
```
sbatch generator.sh
```

2. Run generator script
```
sbatch abaqusjobarray.sh
```

### Find outputs
- Log files found in `logs/` to assess success of the Slurm job.
- Abaqus outputs found in `outputs/outs_<num>`.

