#!/usr/bin/env bash
#PBS -N {{ name }}
#PBS -l select=1:ncpus={{ cpus }}:mpiprocs={{ cpus }}:host={{ host }}
#PBS -l walltime={{ time_limit_hms }}
#PBS -q csed -A g-CSE

export HQ_SERVER_DIR="{{ server_dir }}"

ulimit -c 0
module load openmpi/4.1.1
module load gaussian/16.C.02
module load orca/5.0.4

hq worker start \
    --cpus "{{ cpus }}" \
    --resource "mem=sum({{ mem_mib }})" \
    --on-server-lost "stop" \
    --idle-timeout "{{ idle_timeout }}" \
    --time-limit "{{ time_limit }}"

