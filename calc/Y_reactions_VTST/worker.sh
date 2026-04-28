#!/usr/bin/env bash
#SBATCH --nodes=1
#SBATCH --job-name=worker
#SBATCH --ntasks=4
#SBATCH --mem=20G
#SBATCH --time=72:00:00
#SBATCH --partition=batch
#SBATCH --output=worker.%j.log

export HQ_SERVER_DIR="/home/avcopan/proj/project-cyclopentane/calc/Y_reactions_VTST/.server"

module load gaussian

hq worker start \
    --cpus "4" \
    --resource "mem=sum(19074)" \
    --on-server-lost "stop" \
    --idle-timeout "1 hr" \
    --time-limit "24 hr"
