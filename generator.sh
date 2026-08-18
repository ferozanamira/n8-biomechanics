#!/bin/bash
#SBATCH --job-name=scriptgenerator
#SBATCH --time=02:00:00
#SBATCH --mem=32G
#SBATCH --nodes=1
#SBATCH --ntasks=8

module load miniforge/
conda activate abaqus-env

python script-generator.py