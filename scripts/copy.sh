#!/usr/bin/env bash

DIR=$( dirname -- $( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd ))

TAG_IN=${1}
TAG_OUT=${2}

DIR_IN=${DIR}/${TAG_IN}
DIR_OUT=${DIR}/${TAG_OUT}

mkdir -p ${DIR_OUT}
cp -r ${DIR_IN}/inp ${DIR_OUT}/.
cp ${DIR}/data/mechanalyzer/${TAG_OUT}.csv ${DIR_OUT}/inp/species.csv
cp ${DIR}/data/mechanalyzer/${TAG_OUT}.dat ${DIR_OUT}/inp/mechanism.dat