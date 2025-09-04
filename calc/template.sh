#!/usr/bin/env bash
#PBS -N {{ name }}
#PBS -l select=1:ncpus={{ cpus }}:mpiprocs={{ cpus }}:host={{ host }}
#PBS -l walltime={{ time_limit_hms }}
#PBS -q csed -A g-CSE

export HQ_SERVER_DIR="{{ server_dir }}"

hq worker start \
    --cpus "{{ cpus }}" \
    --resource "mem=sum({{ mem_mib }})" \
    --on-server-lost "stop" \
    --idle-timeout "{{ idle_timeout }}" \
    --time-limit "{{ time_limit }}"

