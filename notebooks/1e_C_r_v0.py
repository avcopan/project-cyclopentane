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

gen_mech = automech.from_smiles(
    spc_smis=["C1=C[CH]CC1", "C1=CC[CH]C1"],
    src_mech=par_mech,
)
#  - H-migrations
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.h_migration_12,
    src_mech=par_mech,
)
#  - Beta scissions (H) (move down to get all)
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.beta_scission_h,
    rcts_=[automech.species.names(gen_mech.species, fml="C5H7")],
    src_mech=par_mech,
)
#  - Ring-opening scissions
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.ring_beta_scission,
    src_mech=par_mech,
)
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.vinyl_ring_beta_scission,
    src_mech=par_mech,
)
#  - Beta scissions
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.beta_scission,
    src_mech=par_mech,
)
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.vinyl_beta_scission,
    src_mech=par_mech,
)
#  - Drop reactions:
gen_mech = automech.drop_species_by_smiles(
    gen_mech,
    smis=[
        # >> H-scission to form ring allene
        "C1=C=CCC1",
    ],
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


