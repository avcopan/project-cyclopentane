#!/bin/env bash
#SBATCH --job-name=dft2
#SBATCH --partition=batch
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mem-per-cpu=20GB
#SBATCH --time=16:00:00
#SBATCH --output=out.log
#SBATCH --error=out.err

#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=username@uga.edu  # Where to send mail (change username@uga.edu to your email address)

eval "$(pixi shell-hook --manifest-path /home/avcopan/proj/project-cyclopentane/code/mechdriver)"
module load gaussian/16-AVX2

automech run
