#!/usr/bin/env bash
set -e  # if any command fails, quit

TYPE=${1}
TAG=${2}
NODE=${3}
EVERY=${4:-1}

DIR=$( dirname -- $( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd ))

WORK_DIR=${DIR}/notebooks

(
    cd ${WORK_DIR}
    pixi run -e proto node ${NODE} logs/${TAG}.log "python -m util.cli simulate ${TYPE} ${TAG} .. -e ${EVERY}"
)
