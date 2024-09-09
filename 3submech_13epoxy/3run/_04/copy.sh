#!/usr/bin/env bash

NUMBER=${1}
TAG=${2:-_full}

mkdir -p inp/
cp ../../../examples/3run/inp/* inp/.
cp ../../2stereoexpand/mechanism${NUMBER}.dat${TAG} inp/mechanism.dat
cp ../../2stereoexpand/species${NUMBER}.csv${TAG} inp/species.csv
