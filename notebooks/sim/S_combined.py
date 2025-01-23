#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pathlib import Path

import util
from util import workflow

browser = True
file = util.notebook_file() if util.is_notebook() else __file__
tag = util.file_tag(file)
root_path = Path("..")
data_path = util.data_path(root_path)


# In[ ]:


# # Build
# import automech

# sub_tags = ["A_rh-oh_p1v0", "B_rh-ho2_p1v1"]
# sub_mechs = [automech.io.read(data_path / f"{t}_raw.json") for t in sub_tags]
# mech = automech.combine_all(sub_mechs)
# print(mech)


# In[ ]:


# # Write
# workflow.write(mech=mech, tag=tag, root_path=root_path, browser=browser)


# In[ ]:


# # Read
# workflow.read(tag=tag, root_path=root_path)


# In[5]:


# Simulate
workflow.simulate(full_tag=f"full_{tag}_calc", root_path=root_path)
workflow.simulate(full_tag=f"full_{tag}_control", root_path=root_path)

