#!/usr/bin/env bash

DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

SUBMECH=${1}
NUMBER=${2}
TAG1=${3:-_sorted}
TAG2=${4:-_new}

SOURCE=${SUBMECH}/2stereoexpand
DEST=${SUBMECH}/3run/${NUMBER}/inp

mkdir -p ${DEST}
# cp ../examples/3run/inp/* ${DEST}/.
cp ${SOURCE}/mechanism${NUMBER}.dat${TAG1} ${DEST}/mechanism.dat
cp ${SOURCE}/species${NUMBER}.csv${TAG2} ${DEST}/species.csv
