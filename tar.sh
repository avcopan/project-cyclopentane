#!/bin/bash
#SBATCH --partition=batch
#SBATCH --job-name=tar
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=4:00:00
#SBATCH --mem=16G

tar --use-compress-program="zstd -T0 -3" -cvf save.tar.zst save

