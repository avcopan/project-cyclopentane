"""General utility functions."""

from pathlib import Path

import IPython


def notebook_prefix() -> str:
    """Determine the prefix of the current IPython notebook."""
    return Path(IPython.get_ipython().user_ns.get("__vsc_ipynb_file__")).stem.split(
        "."
    )[0]
