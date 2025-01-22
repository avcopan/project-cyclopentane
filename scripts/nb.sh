#!/usr/bin/env bash

NOTEBOOK=${1}
NODE=${2}
DIR=${3:-"."}
TAG=$(basename ${NOTEBOOK} .ipynb)

COMMAND="
    export PYTHONPATH=$(pwd):${PYTHONPATH} &&
    python ${DIR}/${TAG}.py
"

jupyter nbconvert --to script ${NOTEBOOK} --output=${DIR}/${TAG}
chmod +x ./${DIR}/${TAG}.py
pixi run node ${NODE} ${DIR}/${TAG}.log "${COMMAND}"
