#!/usr/bin/env bash
set -e  # if any command fails, quit

TYPE=${1}
TAG=${2}
EVERY=${3:-1}

LOG="logs/${TAG}_${TYPE}.log"
echo "LOG=${LOG}"

DIR=$( dirname -- $( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd ))

WORK_DIR=${DIR}/notebooks

(
    cd ${WORK_DIR}
    pixi run -e proto python -u -m util.cli simulate ${TYPE} ${TAG} .. -e ${EVERY} > ${LOG} 2>&1 &
)
