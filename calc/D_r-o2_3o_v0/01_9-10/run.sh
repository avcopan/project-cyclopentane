#!/usr/bin/env bash
export OMP_NUM_THREADS=8
ulimit -c 0
mess mess.inp >> stdout.log &> stderr.log