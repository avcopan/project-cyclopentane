#!/usr/bin/env bash
#SBATCH --partition=batch
#SBATCH --job-name=workflow
#SBATCH --ntasks=1
#SBATCH --time=16:00:00
#SBATCH --mem=10G

PIXI_PATH=/home/avcopan/proj/project-cyclopentane/code/mechdriver

TASK_ENV=$(cat << EOF
$(pixi shell-hook -e dev2 --manifest-path $PIXI_PATH)
module load gaussian/16-AVX2
module load ORCA/5.0.4-gompi-2022a
EOF
)

echo Executing Pixi shell-hook...
eval "$(pixi shell-hook -e dev2 --manifest-path $PIXI_PATH)"
export PYTHONUNBUFFERED=1
mkdir -p .server
export HQ_SERVER_DIR="$(realpath .server)"
echo $HQ_SERVER_DIR

echo Running automech subtasks run...
automech subtasks run -f "--partition=batch" -e "$TASK_ENV" -l "24 hr" $1

