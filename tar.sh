#!/bin/bash
#SBATCH --partition=batch
#SBATCH --job-name=tar
#SBATCH --ntasks=1
#SBATCH --time=6:00:00
#SBATCH --mem=16G

tar --zstd -cvf save.tar.zst save

