#!/usr/bin/env python
from pathlib import Path

import util
from util import workflow

tag = Path(__file__).stem.split(".")[0]
root_path = Path("..")
data_path = util.data_path(root_path)

workflow.simulate(full_tag=f"full_{tag}_calc", root_path=root_path)

workflow.simulate(full_tag=f"full_{tag}_control", root_path=root_path)
