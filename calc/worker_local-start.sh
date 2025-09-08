#!/usr/bin/env bash

hq worker start --cpus 8 --resource "mem=sum(2862)" &
