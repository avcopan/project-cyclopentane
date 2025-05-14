#!/usr/bin/env bash
ulimit -c 0
g16 geom.inp run.out >> stdout.log &> stderr.log
