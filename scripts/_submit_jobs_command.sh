#!/usr/bin/env bash

NODES=${@}
NODES_CSV="$(printf '%s,' ${NODES[@]})"

echo "Running on $(hostname) in $(pwd)" && \
echo "Process ID: $$" && \
echo "Submitting with -n ${NODES_CSV}"  && \
automech subtasks run-adhoc -n ${NODES_CSV} -a "$(pixi shell-hook)"
