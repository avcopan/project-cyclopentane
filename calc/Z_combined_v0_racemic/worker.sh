#!/usr/bin/env bash
#SBATCH --nodes=1
#SBATCH --job-name=worker
#SBATCH --ntasks=32
#SBATCH --mem=120G
#SBATCH --time=04:00:00
#SBATCH --partition=batch
#SBATCH --output=worker.%j.log
#SBATCH --mail-type=ALL
#SBATCH --mail-user=avcopan@uga.edu

export HQ_SERVER_DIR="/home/avcopan/proj/project-cyclopentane/calc/Z_combined_v0/.server"


hq worker start \
    --cpus "32" \
    --resource "mem=sum(114441)" \
    --on-server-lost "stop" \
    --idle-timeout "5 min" \
    --time-limit "4 hr"
