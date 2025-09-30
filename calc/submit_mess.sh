#!/bin/env bash
#SBATCH --job-name=mess
#SBATCH --partition=batch
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=80GB
#SBATCH --time=6:00:00
#SBATCH --output=out.log
#SBATCH --error=out.err

#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=avcopan@uga.edu

eval "$(pixi shell-hook --manifest-path /home/avcopan/proj/project-cyclopentane/code/mechdriver)"

export OMP_NUM_THREADS=8
ulimit -c 0
mess mess.inp >> stdout.log &> stderr.log
