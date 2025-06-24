#!/usr/bin/env python
import re
from pathlib import Path
import pyparsing as pp
import shutil
from collections.abc import Sequence

import click

root_path = Path(__file__).resolve().parents[1]
mess_path_expr: pp.ParseExpression = ... + pp.CaselessKeyword("Writing MESS input file at") + pp.Word(pp.printables)("path")


@click.command()
@click.argument("tags", nargs=-1)
def extract(tags: Sequence[str]):
    """Extract rate and thermo data from subtask dirs."""
    for tag in tags:
        _extract_one(tag)


def _extract_one(tag: str):
    """Extract rate and thermo data from subtask dirs."""
    print(f"Extracting {tag}...")
    path = root_path / "calc" / tag
    ckin_path = path / "CKIN"
    ckin_path.mkdir(exist_ok=True)
    sub_path = path / "subtasks"

    # Extract thermo data
    print("\nExtracting thermo data")
    thermo_files0 = sorted(sub_path.glob("2_*_run_fits/*/CKIN/all_therm.ckin_0"))
    thermo_files1 = sorted(sub_path.glob("2_*_run_fits/*/CKIN/all_therm.ckin_1"))
    assert thermo_files0, f"No thermo files found at {sub_path!s}"
    if thermo_files0:
        thermo_text0 = format_therm_text(
            "\n\n\n".join(list(map(extract_therm_text, thermo_files0)))
        )
        thermo_text1 = format_therm_text(
            "\n\n\n".join(list(map(extract_therm_text, thermo_files1)))
        )

        thermo_file0 = ckin_path / "all_therm.ckin_0"
        thermo_file1 = ckin_path / "all_therm.ckin_1"
        print(f"Writing thermo data to {thermo_file0!s}")
        thermo_file0.write_text(thermo_text0)
        print(f"Writing thermo data to {thermo_file1!s}")
        thermo_file1.write_text(thermo_text1)

    # Extract rate data
    print("\nExtracting rate data")
    rate_files0 = sorted(sub_path.glob("3_*_run_fits/*/CKIN/*.ckin"))
    if not rate_files0:
        print(f"No rate files found at {sub_path!s}")
    for rate_file0 in rate_files0:
        rate_file = ckin_path / rate_file0.name
        print(f"Writing rate data to {rate_file!s}")
        rate_file.write_text(rate_file0.read_text())

    # Extract MESS input data
    print("\nExtracting MESS input data")
    log_files = sorted(sub_path.glob("3_*_write_mess/*/out0.log"))
    assert log_files, f"No log files found at {sub_path!s}"
    for log_file in log_files:
        print(f"Found AutoMech log file at {log_file!s}")
        log_text = log_file.read_text()
        mess_path = Path(mess_path_expr.parse_string(log_text).get("path"))
        mess_inp_file0 = mess_path / "mess.inp"
        assert mess_inp_file0.exists(), mess_inp_file0
        print(f"Found MESS input file at {mess_inp_file0!s}")

        subpes_name = log_file.parent.name
        subpes_path = path / subpes_name
        print(f"Copying MESS run directory to {subpes_path}")
        shutil.copytree(mess_path, subpes_path, dirs_exist_ok=True)
    print("\n")


therm_line_pattern = re.compile(r".*^THER\S*\ *$", flags=re.M)
empty_line_pattern = re.compile(r"\n\s*\n", flags=re.M)
end_line_pattern = re.compile(r"^END", flags=re.M)


def extract_therm_text(therm_file: Path) -> str:
    """Extract the inner contents of a Chemkin thermo file."""
    therm_text = therm_file.read_text()
    therm_text = re.sub(therm_line_pattern, "", therm_text)
    therm_text = re.sub(empty_line_pattern, "\n\n", therm_text)
    therm_text = re.sub(end_line_pattern, "", therm_text)
    return therm_text.strip()


def format_therm_text(therm_text: str) -> str:
    """Format text for a Chemkin thermo file."""
    return f"THERMO\n\n{therm_text}\n\nEND\n\n"


if __name__ == "__main__":
    extract()
