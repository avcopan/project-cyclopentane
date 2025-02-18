"""General utility functions."""

from pathlib import Path

import IPython


def is_notebook() -> bool:
    """Check if this is a notebook."""
    return IPython.get_ipython() is not None


def notebook_file() -> str | None:
    """Get the notebook file path, if this is a notebook."""
    ipy = IPython.get_ipython()
    if ipy is None:
        return None

    return ipy.user_ns.get("__vsc_ipynb_file__")


# Root path functions
def data_path(root_path: str | Path) -> Path:
    """Determine data path from root."""
    return Path(root_path) / "data"


def calc_path(root_path: str | Path, tag: str) -> Path:
    """Determine data path from root."""
    return Path(root_path) / "calc" / tag


def ckin_path(root_path: str | Path, tag: str) -> Path:
    """Determine data path from root."""
    return Path(root_path) / "calc" / tag / "data" / "CKIN"


# Tag functions
def file_tag(file_path: str) -> str:
    """Determine the prefix of the current IPython notebook."""
    return Path(file_path).stem.split(".")[0]


def previous_tags(tag: str) -> list[str]:
    """Determine the previous tags."""
    pre = tag[:-1]
    ver = int(tag[-1])
    return [f"{pre}{i}" for i in range(ver)]


def calculated_mechanism_name(tag: str) -> str:
    """Determine the name of the calculated mechanism."""
    return f"{tag}_calc"


def full_calculated_mechanism_name(tag: str) -> str:
    """Determine the name of the full (merged) calculated mechanism."""
    return f"full_{tag}_calc"


def full_control_mechanism_name(tag: str) -> str:
    """Determine the name of the full (merged) calculated mechanism."""
    return f"full_{tag}_control"
