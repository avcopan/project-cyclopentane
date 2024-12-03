#!/usr/bin/env bash

WORK_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
TEMP_DIR=`mktemp -d -p "$WORK_DIR"`

mechanalyzer sort -m orig_mechanism.dat -o mechanism.dat -c $TEMP_DIR/sort_species.csv

rm -r $TEMP_DIR
