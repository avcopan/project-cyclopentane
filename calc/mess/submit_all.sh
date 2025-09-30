#!/usr/bin/env bash

module load parallel
ls -d */ | parallel 'cd {} && sbatch submit_mess.sh'

