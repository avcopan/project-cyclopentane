# %%
from pathlib import Path

import automech
from project_utilities import p_, util, workflow

file = util.notebook_file() if util.is_notebook() else __file__
tag = util.file_tag(file)
root_path = Path("..")
par_mech = workflow.read_parent_mechanism(root_path=root_path)

# %%
# Generate submechanism
from automol.graph import enum

from automech.species import Species

gen_mech = automech.from_smiles(spc_smis=["C1=CCCC1"], src_mech=par_mech)
#  - Abstractions
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.abstraction,
    rcts_=["C1=CCCC1", "O[O]"],
    spc_col_=Species.smiles,
    src_mech=par_mech,
)
#  - Additions
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.pi2_addition,
    rcts_=["C1=CCCC1", "O[O]"],
    spc_col_=Species.smiles,
    src_mech=par_mech,
)
#  - Ring-forming scissions
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.qooh_ring_forming_scission,
    src_mech=par_mech,
)

automech.display(gen_mech)

# %%
# Expand stereochemistry
ste_mech, *_, gen_mech = workflow.expand_stereo(
    mech=gen_mech, tag=tag, root_path=root_path
)

# %%
# Prepare calculation
workflow.prepare_calculation(
    gen_mech=gen_mech, ste_mech=ste_mech, tag=tag, root_path=root_path
)


