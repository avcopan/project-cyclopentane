#!/usr/bin/env python
import re
from pathlib import Path

import click

root_path = Path(__file__).resolve().parents[1]


@click.command()
@click.argument("tag")
def extract(tag: str):
    """Extract rate and thermo data from subtask dirs."""
    print(f"Extracting {tag}...")
    path = root_path / "calc" / tag
    ckin_path = path / "CKIN"
    ckin_path.mkdir(exist_ok=True)

    # Read thermo data
    thermo_path = path / "subtasks"
    thermo_files0 = sorted(thermo_path.glob("2_*_run_fits/*/CKIN/all_therm.ckin_0"))
    thermo_files1 = sorted(thermo_path.glob("2_*_run_fits/*/CKIN/all_therm.ckin_1"))
    if thermo_files0:
        thermo_text0 = format_therm_text(
            "\n\n\n".join(list(map(extract_therm_text, thermo_files0)))
        )
        thermo_text1 = format_therm_text(
            "\n\n\n".join(list(map(extract_therm_text, thermo_files1)))
        )

        # Write thermo data
        thermo_file0 = ckin_path / "all_therm.ckin_0"
        thermo_file1 = ckin_path / "all_therm.ckin_1"
        print(f"Writing thermo data to {thermo_file0!s}")
        thermo_file0.write_text(thermo_text0)
        print(f"Writing thermo data to {thermo_file1!s}")
        thermo_file1.write_text(thermo_text1)

    # Read/write rate data
    rate_path = path / "subtasks"
    rate_files0 = sorted(rate_path.glob("3_*_run_fits/*/CKIN/*.ckin"))
    for rate_file0 in rate_files0:
        rate_file = ckin_path / rate_file0.name
        print(f"Writing rate data to {rate_file!s}")
        rate_file.write_text(rate_file0.read_text())


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
