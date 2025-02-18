#!/usr/bin/env python
import sys

import automol

args = sys.argv

# smi = "C1=CCCC1"
smi = args[1]
chi = automol.smiles.amchi(smi)
name = args[2] if len(args) > 2 else automol.amchi.chemkin_name(chi)
smi = automol.amchi.smiles(chi)
ich = automol.smiles.inchi(smi)
ick = automol.inchi.inchi_key(ich)
mult = automol.amchi.guess_spin(chi) + 1
char = 0
cchi = automol.chi.canonical_enantiomer(ich)

print(f"'{name}','{smi}','{ich}','{ick}',{mult},{char},'{cchi}'")
