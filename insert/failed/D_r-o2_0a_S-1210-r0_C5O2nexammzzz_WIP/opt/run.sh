#!/usr/bin/env bash
ulimit -c 0
g16 run.inp_2.23 run.out_2.23 >> stdout.log &> stderr.log