#!/bin/bash
#SBATCH --partition=batch
#SBATCH --job-name=automech
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --time=36:00:00
#SBATCH --mem-per-cpu=36G

#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=avcopan@uga.edu

eval "$(pixi shell-hook -e dev2 --manifest-path /home/avcopan/proj/project-cyclopentane/code/mechdriver)"
export PYTHONUNBUFFERED=1
module load ORCA/5.0.4-gompi-2022a

automech run 

