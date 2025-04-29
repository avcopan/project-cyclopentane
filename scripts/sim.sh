#!/usr/bin/env bash
set -e  # if any command fails, quit

TAG=${1}
NODE=${2}
EVERY=${3:-1}

DIR=$( dirname -- $( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd ))

WORK_DIR=${DIR}/notebooks

(
    cd ${WORK_DIR}
    pixi run node ${NODE} logs/${TAG}.log "python -m util.simulate ${TAG} .. -e ${EVERY}"
)
