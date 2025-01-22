#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pathlib import Path

import util
from util import workflow

file = util.notebook_file() if util.is_notebook() else __file__
tag = util.file_tag(file)
root_path = Path("..")
data_path = util.data_path(root_path)


# In[ ]:


# # Build
# from automol.graph import enum

# import automech
# from automech.schema import Species

# mech0 = automech.io.read(data_path / "full_raw.json")
# mech = automech.from_smiles(spc_smis=["C1=CCCC1", "C12C(O2)CCC1"], src_mech=mech0)
# #  - add HO2 addition to *ene*
# mech = automech.enumerate_reactions(
#     mech,
#     enum.ReactionSmarts.pi2_addition,
#     rcts_=[None, "O[O]"],
#     spc_col_=Species.smiles,
#     src_mech=mech0,
# )
# #  - add ring-forming scission
# mech = automech.enumerate_reactions(
#     mech,
#     enum.ReactionSmarts.ring_forming_scission,
#     src_mech=mech0,
# )
# #  - enumerate HO2 abstractions from *ene* and *1-2epoxy*
# mech = automech.enumerate_reactions(
#     mech,
#     enum.ReactionSmarts.abstraction,
#     rcts_=[["C1=CCCC1", "C12C(O2)CCC1"], "O[O]"],
#     spc_col_=Species.smiles,
#     src_mech=mech0,
# )


# In[ ]:


# # Write
# workflow.write(mech=mech, tag=tag, root_path=root_path)


# In[ ]:


# # Read
# workflow.read(tag=tag, root_path=root_path)


# In[5]:


# Simulate
workflow.simulate(full_tag=f"full_{tag}_calc", root_path=root_path)
workflow.simulate(full_tag=f"full_{tag}_control", root_path=root_path)

