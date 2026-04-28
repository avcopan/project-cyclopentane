#!/usr/bin/env bash
#SBATCH --nodes=1
#SBATCH --job-name=run
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --time=144:00:00
#SBATCH --partition=batch
#SBATCH --output=run.log

TASK_ENV=$(cat << EOF
$(pixi shell-hook -e dev2 --manifest-path /home/avcopan/proj/project-cyclopentane/code/mechdriver)
module load gaussian/16-AVX2
module load ORCA/5.0.4-gompi-2022a
EOF
)

eval "$(pixi shell-hook -e dev2 --manifest-path "/home/avcopan/proj/project-cyclopentane/code/mechdriver")"

mechdriver subtasks run -e "$TASK_ENV"

