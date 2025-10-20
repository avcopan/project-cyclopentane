#!/usr/bin/env bash

ls -d */ | parallel 'cd {} && sbatch submit_mess.sh'

