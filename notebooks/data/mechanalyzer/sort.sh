#!/usr/bin/env bash
PREFIX_IN=${1}
PREFIX_OUT=${2}

mechanalyzer sort \
    -m ${PREFIX_IN}mechanism.dat \
    -s ${PREFIX_IN}species.csv \
    -o ${PREFIX_OUT}mechanism.dat \
    -c ${PREFIX_OUT}species.csv

# Overwrite the re-ordered species CSV file
cp ${PREFIX_IN}species.csv ${PREFIX_OUT}species.csv

