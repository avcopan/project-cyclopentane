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
    rcts_=["C1=CCCC1", "[OH]"],
    spc_col_=Species.smiles,
    src_mech=par_mech,
)
#  - Additions
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.pi2_addition,
    rcts_=["C1=CCCC1", "[OH]"],
    spc_col_=Species.smiles,
    src_mech=par_mech,
)
#   - H-migrations
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.h_migration_12,
    rcts_=[automech.species.names(gen_mech.species, fml="C5H9O")],
    src_mech=par_mech,
)
#  - Beta scissions (H) (move down to get all)
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.beta_scission_h,
    rcts_=[automech.species.names(gen_mech.species, fml="C5H9O")],
    src_mech=par_mech,
)
#  - Ring-opening scissions
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.ring_beta_scission,
    rcts_=["C1(O)[CH]CCC1"],
    spc_col_=Species.smiles,
    src_mech=par_mech,
)
#  - Beta scissions
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.beta_scission,
    src_mech=par_mech,
)
automech.display(gen_mech)

# %%
# Expand stereochemistry
ste_mech, *_, gen_mech = workflow.expand_stereo(
    mech=gen_mech, tag=tag, root_path=root_path
)

#  - Drop stereo-specific reactions
ste_mech = automech.drop_reactions_by_smiles(
    ste_mech,
    rxn_smis=[
        # >> 1,3 migration (created by symmetry)
        r"O[C@H]1[CH]CCC1>>O[C@@H]1C[CH]CC1",
        r"O[C@@H]1[CH]CCC1>>O[C@H]1C[CH]CC1",
    ],
)

# %%
# Prepare calculation
workflow.prepare_calculation(
    gen_mech=gen_mech, ste_mech=ste_mech, tag=tag, root_path=root_path
)


