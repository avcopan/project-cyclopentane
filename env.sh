#!/usr/bin/env bash

PIXI_PATH="/home/avcopan/proj/project-cyclopentane/code/mechdriver"

eval "$(pixi shell-hook -e dev2 --manifest-path $PIXI_PATH)"

which python

