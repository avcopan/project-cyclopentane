#!/usr/bin/env bash
#SBATCH --nodes=1
#SBATCH --job-name=worker
#SBATCH --ntasks=4
#SBATCH --mem=144G
#SBATCH --time=72:00:00
#SBATCH --partition=batch
#SBATCH --output=worker.%j.log
#SBATCH --mail-type=ALL
#SBATCH --mail-user=avcopan@uga.edu

export HQ_SERVER_DIR="/home/avcopan/proj/project-cyclopentane/calc/X_species_v0/.server"


hq worker start \
    --cpus "4" \
    --resource "mem=sum(137330)" \
    --on-server-lost "stop" \
    --idle-timeout "5 min" \
    --time-limit "24 hr"
