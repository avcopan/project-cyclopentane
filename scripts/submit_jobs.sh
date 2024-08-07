#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

read -a NODES <<< "${@}"
FIRST_NODE=${NODES[0]}

ACTIVATION_HOOK="$(pixi shell-hook)"
ECHO_REMOTE_INFO_COMMAND='echo "Hello from $(hostname) at $(pwd)"'
WRITE_PID_COMMAND='echo $! > pid.txt'

ssh ${FIRST_NODE} /bin/env bash << EOF
    cd $(pwd)
    eval ${ACTIVATION_HOOK@Q}
    eval ${ECHO_REMOTE_INFO_COMMAND@Q}
    nohup ${SCRIPT_DIR}/_submit_jobs_command.sh ${NODES[@]} > sub.log 2>&1 &
    eval ${WRITE_PID_COMMAND@Q}
EOF
