#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pathlib import Path

import util
from util import workflow

browser = False
file = util.notebook_file() if util.is_notebook() else __file__
tag = util.file_tag(file)
root_path = Path("..")
data_path = util.data_path(root_path)


# In[ ]:


# # Build
# from automol.graph import enum

# import automech
# from automech.species import Species

# mech0 = automech.io.read(data_path / "full_raw.json")
# mech = automech.from_smiles(spc_smis=["C1=CCCC1"], src_mech=mech0)
# #  - add OH addition to *ene*
# mech = automech.enumerate_reactions(
#     mech,
#     enum.ReactionSmarts.pi2_addition,
#     rcts_=[None, "[OH]"],
#     spc_col_=Species.smiles,
#     src_mech=mech0,
# )
# #  - add H-migrations
# mech = automech.enumerate_reactions(
#     mech,
#     enum.ReactionSmarts.h_migration,
#     spc_col_=Species.smiles,
#     src_mech=mech0,
#     repeat=2
# )
# #  - add ring beta scissions
# mech = automech.enumerate_reactions(
#     mech,
#     enum.ReactionSmarts.ring_beta_scission,
#     src_mech=mech0,
# )


# In[ ]:


# # Write
# workflow.write(mech=mech, tag=tag, root_path=root_path, browser=browser)


# In[ ]:


# # Read
# workflow.read(tag=tag, root_path=root_path)


# In[ ]:


# Simulate
workflow.simulate(full_tag=f"full_{tag}_calc", root_path=root_path)
workflow.simulate(full_tag=f"full_{tag}_control", root_path=root_path)

