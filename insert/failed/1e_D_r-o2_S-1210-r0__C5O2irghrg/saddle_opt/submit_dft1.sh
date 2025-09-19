#!/bin/env bash
#SBATCH --job-name=Y78_const_opt
#SBATCH --partition=batch
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mem-per-cpu=2700mb
#SBATCH --time=16:00:00
#SBATCH --output=out.log
#SBATCH --error=out.err

#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=username@uga.edu  # Where to send mail (change username@uga.edu to your email address)

module load gaussian/16-AVX2

ulimit -c 0
g16 run.inp run.out >> stdout.log &> stderr.log
