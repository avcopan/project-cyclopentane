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
from automech.species import Species
from automol.graph import enum

gen_mech = automech.from_smiles(
    spc_smis=["[CH]1CCCC1"],
    src_mech=par_mech,
)
#  - Additions
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.o2_addition,
    rcts_=[None, "[O][O]"],
    spc_col_=Species.smiles,
    src_mech=par_mech,
)
#  - Eliminations
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.ho2_elimination,
    spc_col_=Species.smiles,
    src_mech=par_mech,
)
#  - Migrations
gen_mech = automech.enumerate_reactions(
    gen_mech, enum.ReactionSmarts.qooh_formation, src_mech=par_mech
)
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.h_migration_12,
    src_mech=par_mech,
    rcts_=[automech.species.names(gen_mech.species, fml="C5H9O2")],
    excl_rcts=automech.unstable_species_names(gen_mech),
)
#   - Ring-forming scissions
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.qooh_ring_forming_scission,
    src_mech=par_mech,
    excl_rcts=automech.unstable_species_names(gen_mech),
)
#  - Ring-opening scissions
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.ring_beta_scission,
    src_mech=par_mech,
    rcts_=[automech.species.names(gen_mech.species, fml="C5H9O2")],
    excl_rcts=automech.unstable_species_names(gen_mech),
)
#  - Beta scissions
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.beta_scission,
    src_mech=par_mech,
    rcts_=[automech.species.names(gen_mech.species, fml="C5H9O2")],
    excl_rcts=automech.unstable_species_names(gen_mech),
)
#  - Vinyl beta scissions
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.vinyl_beta_scission,
    src_mech=par_mech,
    rcts_=[automech.species.names(gen_mech.species, fml="C5H9O2")],
    excl_rcts=automech.unstable_species_names(gen_mech),
)
#  - Resonance-stabilized instability reactions
gen_mech = automech.enumerate_reactions(
    gen_mech,
    enum.ReactionSmarts.resonant_qooh_instability,
    src_mech=par_mech,
    match_src=False,
)
#  - Instability products
gen_mech = automech.enumerate_products(
    gen_mech,
    enum.ReactionSmarts.qooh_instability,
    src_mech=par_mech,
)
#  - Drop reactions:
gen_mech = automech.drop_species_by_smiles(
    gen_mech,
    smis=[
        # >> beta-QOOH -> alpha-QOOH H-migration (product)
        "OO[C]1CCCC1",
    ],
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
        r"OO[C@H]1[CH]CCC1>>OO[C@@H]1C[CH]CC1",
        r"OO[C@@H]1[CH]CCC1>>OO[C@H]1C[CH]CC1",
    ],
)

# %%
# Prepare calculation
workflow.prepare_calculation(
    gen_mech=gen_mech, ste_mech=ste_mech, tag=tag, root_path=root_path
)


