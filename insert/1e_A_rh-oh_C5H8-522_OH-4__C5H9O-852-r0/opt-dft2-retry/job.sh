#!/bin/bash
#SBATCH --partition=batch
#SBATCH --job-name=test
#SBATCH --ntasks=6
#SBATCH --ntasks-per-node=6
#SBATCH --cpus-per-task=1
#SBATCH --time=72:00:00
#SBATCH --mem-per-cpu=40G
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=avcopan@uga.edu

module load gaussian/16-AVX2
ulimit -c 0
g16 run.inp run.out
