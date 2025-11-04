#!/bin/bash
#SBATCH --partition=batch
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mem-per-cpu=5G
#SBATCH --time=24:00:00

#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=avcopan@uga.edu

echo Activating environment...
eval "$(pixi shell-hook -e all --manifest-path /home/avcopan/proj/project-cyclopentane/code/protomech)"

echo Running simulation script...
putils simulate "$@"

