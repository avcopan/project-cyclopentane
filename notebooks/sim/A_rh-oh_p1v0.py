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
# mech = automech.from_smiles(spc_smis=["C1=CCCC1", "C12C(O2)CCC1"], src_mech=mech0)
# #  - enumerate OH abstractions from *ene* and *1-2epoxy*
# mech = automech.enumerate_reactions(
#     mech,
#     enum.ReactionSmarts.abstraction,
#     rcts_=[None, "[OH]"],
#     spc_col_=Species.smiles,
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


# In[ ]:


# # Plot
# charts = workflow.plot(
#     full_tag=f"full_{tag}_calc",
#     x_col="O2_molecules",
#     y_col_=["C5H8(522)", "C5H8O(825)rs"],
#     root_path=root_path,
#     line_source_=["hill", "lokachari"],
#     point_source="experiment",
# )
# for chart in charts:
#     chart.show()

