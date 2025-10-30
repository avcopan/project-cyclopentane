#!/bin/bash
#SBATCH --partition=batch
#SBATCH --job-name=automech
#SBATCH --ntasks=1
#SBATCH --time=12:00:00
#SBATCH --mem=10G

#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=avcopan@uga.edu

eval "$(pixi shell-hook -e dev2 --manifest-path /home/avcopan/proj/project-cyclopentane/code/mechdriver)"
export PYTHONUNBUFFERED=1
module load gaussian/16-AVX2
module load ORCA/5.0.4-gompi-2022a

automech run 

