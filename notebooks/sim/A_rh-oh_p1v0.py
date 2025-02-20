from pathlib import Path

import util
from util import workflow

file = util.notebook_file() if util.is_notebook() else __file__
tag = util.file_tag(file)
root_path = Path("..")

workflow.simulate(full_tag=f"full_{tag}_calc", root_path=root_path)
workflow.simulate(full_tag=f"full_{tag}_control", root_path=root_path)
