#!/usr/bin/env bash
#SBATCH --nodes=1
#SBATCH --job-name=server
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --time=24:00:00
#SBATCH --partition=batch
#SBATCH --output=server.log

export HQ_SERVER_DIR="/home/avcopan/proj/project-cyclopentane/calc/W_basis/.server"

hq server start

