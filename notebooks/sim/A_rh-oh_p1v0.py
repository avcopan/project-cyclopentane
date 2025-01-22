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


# In[2]:


# # Build
# from automol.graph import enum

# import automech
# from automech.schema import Species

# mech0 = automech.io.read(data_path / "full_raw.json")
# mech = automech.from_smiles(spc_smis=["C1=CCCC1", "C12C(O2)CCC1"], src_mech=mech0)
# #  - enumerate OH abstractions from *ene* and *1-2epoxy*
# mech = automech.enumerate_reactions(
#     mech,
#     enum.ReactionSmarts.abstraction,
#     rcts_=[None, "[OH]"],
#     spc_col_=Species.smiles,
#     src_mech=mech0,
# )


# In[3]:


# # Write
# workflow.write(mech=mech, tag=tag, root_path=root_path)


# In[ ]:


# # Read
# workflow.read(tag=tag, root_path=root_path)


# In[5]:


# Simulate
workflow.simulate(full_tag=f"full_{tag}_calc", root_path=root_path)
workflow.simulate(full_tag=f"full_{tag}_control", root_path=root_path)

