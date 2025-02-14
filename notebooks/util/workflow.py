"""Project workflows."""

import functools
from collections.abc import Sequence
from numbers import Number
from pathlib import Path

import altair
import cantera
import polars
from cantera.ck2yaml import Parser

import automech
from automech import Mechanism
from automech.species import Species
from automech.util import c_

from ._util import ckin_path as ckin_path_
from ._util import data_path as data_path_
from .sim import reactors


# Workflows
def write(
    mech: Mechanism, tag: str, root_path: str | Path, browser: bool = False
) -> None:
    """Write mechanism for calculation.

    :param mech: Mechanism
    :param tag: Mechanism tag
    :param root_path: Project root directory
    :param browser: Open browser to visualize mechanism
    """
    mech0 = mech
    data_path = data_path_(root_path)

    # Display
    print("\nFinalizing build for...")
    print(mech0)
    if browser:
        automech.display(mech0)

    # Expand and sort
    print("\nExpanding stereochemistry...")
    mech, err_mech = automech.expand_stereo(mech0, distinct_ts=False)
    mech = automech.with_sort_data(mech)

    # Write
    print("\nWriting mechanism...")
    json_path0 = data_path / f"{tag}_raw.json"
    json_path = data_path / f"{tag}.json"
    reac_path = data_path / "mechanalyzer" / f"{tag}.dat"
    spec_path = data_path / "mechanalyzer" / f"{tag}.csv"
    print(json_path0)
    automech.io.write(mech0, json_path0)
    print(json_path)
    automech.io.write(mech, json_path)
    print(reac_path)
    print(spec_path)
    automech.io.mechanalyzer.write.mechanism(mech, rxn_out=reac_path, spc_out=spec_path)

    # Display
    print("\nStereoexpansion errors:")
    automech.display_reactions(err_mech)


def read(tag: str, root_path: str | Path) -> None:
    """Read calculation results.

    :param tag: Mechanism tag
    :param root_path: Project root directory
    """
    data_path = data_path_(root_path)
    ckin_path = ckin_path_(root_path, tag)

    # Read mechanisms
    print("\nReading mechanisms...")
    par_mech = automech.io.read(data_path / "full_raw.json")
    cal_mech0 = automech.io.read(data_path / f"{tag}.json")

    # Add calculated thermo to mechanism object
    print("\nAdding calculated thermo...")
    *_, therm_file = ckin_path.glob("all_therm.ckin*")
    cal_mech = automech.io.chemkin.update.thermo(cal_mech0, therm_file)

    # Add calculated rates to mechanism object (use units of parent)
    print("\nAdding calculated rates...")
    rate_files = list(ckin_path.glob("*.ckin"))
    cal_mech = automech.io.chemkin.update.rates(cal_mech, rate_files)

    # Merge updated rates and thermo into parent mechanism
    print("\nExpanding and updating parent...")
    mech0 = automech.expand_parent_stereo(par_mech, cal_mech)
    mech = automech.update(mech0, cal_mech)

    # Write
    print("\nWriting mechanism...")
    part = f"{tag}_calc"
    full0 = f"full_{tag}_control"
    full = f"full_{tag}_calc"
    print(data_path / f"{part}.json")
    automech.io.write(cal_mech, data_path / f"{part}.json")
    print(data_path / f"{full0}.json")
    automech.io.write(mech0, data_path / f"{full0}.json")
    print(data_path / f"{full}.json")
    automech.io.write(mech, data_path / f"{full}.json")
    print(data_path / "chemkin" / f"{full0}.dat")
    automech.io.chemkin.write.mechanism(mech0, data_path / "chemkin" / f"{full0}.dat")
    print(data_path / "chemkin" / f"{full}.dat")
    automech.io.chemkin.write.mechanism(mech, data_path / "chemkin" / f"{full}.dat")

    # Compare calculated to parent mechanism
    print("\nCompare calculated mechanism to parent mechanism...")
    automech.display_reactions(
        cal_mech, comp_mechs=[par_mech], comp_labels=["Hill"], comp_stereo=False
    )


def simulate(
    full_tag: str,
    root_path: str | Path,
    temp_k: Number = 825,
    pres_atm: Number = 1.1,
    tau_s: Number = 4,
    vol_cm3: Number = 1,
    gather_every: int = 1,
) -> None:
    """Simulate model (JSR).

    :param tag: Mechanism tag
    :param root_path: Project root directory
    :param temp_k: Temperature in K
    :param pres_atm: Pressure in atm
    :param tau_s: Residence time in s
    :param vol_cm3: Volume in cm^3
    :param gather_every: Gather every nth point
    """
    data_path = data_path_(root_path)

    # Read in data and rename species to match simulation
    print("\nReading in species...")
    spc_df0 = polars.read_csv(data_path / "hill" / "species.csv")
    spc_df = automech.species(automech.io.read(data_path / f"{full_tag}.json"))
    name_col = Species.name
    name_col0 = c_.orig(name_col)
    spc_df = spc_df.select(name_col, name_col0).join(spc_df0, on=name_col0, how="left")
    spc_df = spc_df.filter(polars.col("hill").is_not_null())
    print(spc_df)

    # Read in concentration data
    print("\nReading in concentrations...")
    conc_df = polars.read_csv(data_path / "hill" / "concentration.csv")
    conc_df = conc_df.gather_every(gather_every)
    print(conc_df)

    # Determine concentrations for each point
    print("\nDetermining concentrations for each point...")
    spc_dct = dict(spc_df.select("concentration", name_col0).drop_nulls().iter_rows())
    concs = conc_df.rename(spc_dct).select("CPT(563)", "N2", "O2(6)").rows(named=True)
    print(concs)

    # Read in ChemKin mechanism and convert to Cantera
    print("\nConverting ChemKin mechanism to Cantera YAML...")
    Parser.convert_mech(
        data_path / "chemkin" / f"{full_tag}.dat",
        out_name=data_path / "cantera" / f"{full_tag}.yaml",
    )

    # Load mechanism and set initial conditions
    print("\nDefining model and conditions...")
    model = cantera.Solution(data_path / "cantera" / f"{full_tag}.yaml")
    pres_atm *= cantera.one_atm  # convert to Pa from atm
    vol_cm3 *= (1e-2) ** 3  # convert to m^3 from cm^3

    # Run simulations for each point and store the results in an array
    print("\nRunning simulations...")
    solns = cantera.SolutionArray(model)
    for conc in concs:
        print(f"Starting simulation for {conc}")
        reactor = reactors.jsr(
            model=model, temp=temp_k, pres=pres_atm, tau=tau_s, vol=vol_cm3, conc=conc
        )
        solns.append(reactor.thermo.state)

    print("\nExtracting results...")
    sim_df = conc_df.with_columns(
        polars.Series(s, solns(s).X.flatten() * 10**6) for s in spc_df[name_col]
    )
    print(sim_df)

    print("\nWriting results to CSV...")
    print(data_path / "cantera" / f"{full_tag}_species.csv")
    print(data_path / "cantera" / f"{full_tag}.csv")
    spc_df.write_csv(data_path / "cantera" / f"{full_tag}_species.csv")
    sim_df.write_csv(data_path / "cantera" / f"{full_tag}.csv")


def plot(
    full_tag: str,
    root_path: str | Path,
    x_col: str,
    y_col_: str | Sequence[str],
    line_source_: str | Sequence[str] | None = None,
    point_source: str | None = None,
    my_work_label: str = "this work",
) -> list[altair.Chart]:
    """Plot simulation results.

    :param tag: Mechanism tag
    :param root_path: Project root directory
    :param line_source_: Extra data source(s) to plot as line(s)
    :param point_source: Extra data source to plot as points
    :return: Altair chart
    """
    data_path = data_path_(root_path)
    line_source_ = [] if line_source_ is None else line_source_
    line_sources = [line_source_] if isinstance(line_source_, str) else line_source_
    sources = [*line_sources, point_source] if point_source else line_sources

    name_df = polars.read_csv(data_path / "cantera" / f"{full_tag}_species.csv")
    data_dct = {s: polars.read_csv(data_path / "hill" / f"{s}.csv") for s in sources}
    data_dct = {s: rename_columns(s, d, name_df) for s, d in data_dct.items()}
    data_dct[my_work_label] = polars.read_csv(data_path / "cantera" / f"{full_tag}.csv")
    line_sources.insert(0, my_work_label)

    y_cols = [y_col_] if isinstance(y_col_, str) else y_col_
    charts = [
        make_chart(data_dct, x_col, y_col, line_sources, point_source)
        for y_col in y_cols
    ]
    return charts


def rename_columns(
    source: str, data_df: polars.DataFrame, name_df: polars.DataFrame
) -> polars.DataFrame:
    """Preprocess data for plotting.

    :param source: Data source
    :param data_df: Simulation data
    :param name_df: Species names
    :return: Preprocessed data
    """
    col_dct = dict(name_df.select(source, "name").drop_nulls().iter_rows())
    col_dct.update({f"{n0}_err": f"{n}_err" for n0, n in col_dct.items()})
    col_dct = {n0: n for n0, n in col_dct.items() if n0 in data_df.columns}
    return data_df.rename(col_dct)


def isolate_xy_columns(
    source: str, data_df: polars.DataFrame | None, x_col: str, y_col: str
) -> polars.DataFrame:
    """Isolate x and y columns.

    :param source: Data source
    :param data_df: Data
    :param x_col: X-axis column
    :param y_col: Y-axis column
    :return: Isolated data
    """
    if data_df is None:
        return None

    return data_df.select(x_col, y_col).rename({y_col: source})


def make_chart(
    data_dct: dict[str, polars.DataFrame],
    x_col: str,
    y_col: str,
    line_sources: Sequence[str],
    point_source: str | None = None,
) -> altair.Chart:
    """Make an altair chart for one variable.

    :param data_dct: Data sources
    :param x_col: X-axis column
    :param y_col: Y-axis column
    :param line_sources: Data sources to plot as lines
    :param point_source: Extra data source to plot as points
    :return: Joined data
    """
    line_dfs = [
        isolate_xy_columns(s, data_dct.get(s), x_col, y_col) for s in line_sources
    ]
    point_df = isolate_xy_columns(
        point_source, data_dct.get(point_source), x_col, y_col
    )

    line_df = functools.reduce(lambda x, y: x.join(y, on=x_col), line_dfs)

    point_chart = (
        altair.Chart(point_df)
        .mark_circle()
        .encode(x=x_col, y=point_source, color=altair.value("black"))
    )
    line_chart = (
        altair.Chart(line_df)
        .mark_line()
        .transform_fold(fold=line_sources)
        .encode(x=x_col, y="value:Q", color="key:N")
    )
    return line_chart + point_chart
