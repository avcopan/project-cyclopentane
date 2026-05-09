#!/usr/bin/env bash
#SBATCH --nodes=1
#SBATCH --job-name=server
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --time=144:00:00
#SBATCH --partition=batch
#SBATCH --output=server.%j.log

export HQ_SERVER_DIR="/home/avcopan/proj/project-cyclopentane/calc/Z_combined_v0/.server"

hq server start

