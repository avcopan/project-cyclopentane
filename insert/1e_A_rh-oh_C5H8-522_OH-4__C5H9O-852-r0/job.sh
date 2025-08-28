#!/bin/bash
#SBATCH --partition=batch
#SBATCH --job-name=test
#SBATCH --ntasks=6
#SBATCH --ntasks-per-node=6
#SBATCH --cpus-per-task=1
#SBATCH --time=1:00:00
#SBATCH --mem-per-cpu=12G
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=avcopan@uga.edu

module load gaussian/16-AVX2
module load ORCA/5.0.4-gompi-2022a
eval "$(pixi shell-hook --manifest-path /home/avcopan/proj/project-cyclopentane/code/mechdriver)"

automech run
