#!/usr/bin/env bash
NUMBER=${1}

mechanalyzer sort \
    -m mechanism${NUMBER}.dat_new \
    -s species${NUMBER}.csv_new \
    -o mechanism${NUMBER}.dat_sorted \
    -c species${NUMBER}.csv_sorted

