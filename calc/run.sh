TASK_ENV=$(cat << EOF
$(pixi shell-hook -e dev2 --manifest-path /home/avcopan/proj/project-cyclopentane/code/mechdriver)
module load gaussian/16-AVX2
module load ORCA/5.0.4-gompi-2022a
EOF
)

automech subtasks run -f "--partition=batch" -e "$TASK_ENV"
