#!/usr/bin/env bash
ulimit -c 0
g16 run.inp_2.225 run.out_2.225 >> stdout.log &> stderr.log
