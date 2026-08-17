!/bin/bash
#SBATCH --job-name=jobtest
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --array=1-3          # Submit jobs 1 through 3
#SBATCH --output=logs/job_%A_%a.out # %A = array job ID, %a = task ID

# load the abaqus
module load abaqus/2022

# license
export LM_LICENSE_FILE=27004@abaqus-server1.LEEDS.AC.UK
export ABAQUSLM_LICENSE_FILE=$LM_LICENSE_FILE

OUTDIR="$PWD/output/outs_${SLURM_ARRAY_TASK_ID}"
# make output directory
mkdir -p "$OUTDIR"
# move into output directory
cd "$OUTDIR"
# Process different input files
PYTHON_FILE="/scratch/bs232nc/n8-internship/example_${SLURM_ARRAY_TASK_ID}.py"
# submit abaqus
abaqus cae nogui="$PYTHON_FILE"
