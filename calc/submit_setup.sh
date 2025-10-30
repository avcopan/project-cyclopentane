#!/bin/bash
#SBATCH --partition=batch
#SBATCH --job-name=setup
#SBATCH --ntasks=1
#SBATCH --time=1:00:00
#SBATCH --mem=2G

#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=avcopan@uga.edu

echo Executing Pixi shell-hook...
eval "$(pixi shell-hook -e dev2 --manifest-path /home/avcopan/proj/project-cyclopentane/code/mechdriver)"
export PYTHONUNBUFFERED=1

echo Running automech subtasks setup...
automech subtasks setup

