"""Project workflows."""

import functools
import signal
import time
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

from . import p_
from ._util import (
    previous_tags,
)
from .sim import reactors


# Workflows
def write_parent_mechanism(mech: Mechanism, root_path: str | Path) -> None:
    """Write parent mechanism.

    :param mech: Parent mechanism
    :param root_path: Project root directory
    """
    mech_path = p_.parent_mechanism(ext="json", path=p_.data(root_path))
    return automech.io.write(mech, mech_path)


def read_parent_mechanism(root_path: str | Path) -> Mechanism:
    """Read parent mechanism.

    :param root_path: Project root directory
    :return: Parent mechanism
    """
    mech_path = p_.parent_mechanism(ext="json", path=p_.data(root_path))
    return automech.io.read(mech_path)


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

    # Display
    print("\nFinalizing build for...")
    print(mech0)
    if browser:
        automech.display(mech0)

    # Dropping duplicate reactions
    mech = automech.drop_duplicate_reactions(mech0)

    # Expand and sort
    print("\nExpanding stereochemistry...")
    mech, err_mech = automech.expand_stereo(mech, distinct_ts=False)
    mech = automech.with_sort_data(mech)

    # Write
    print("\nWriting mechanism...")
    mech0_path = p_.original_mechanism(tag, ext="json", path=p_.data(root_path))
    mech_path = p_.mechanism(tag, ext="json", path=p_.data(root_path))
    mech_rxn_path = p_.mechanism(tag, ext="dat", path=p_.mechanalyzer(root_path))
    mech_spc_path = p_.mechanism(tag, ext="csv", path=p_.mechanalyzer(root_path))
    print(mech0_path)
    automech.io.write(mech0, mech0_path)
    print(mech_path)
    automech.io.write(mech, mech_path)
    print(mech_rxn_path)
    print(mech_spc_path)
    automech.io.mechanalyzer.write.mechanism(
        mech, rxn_out=mech_rxn_path, spc_out=mech_spc_path
    )

    # Display
    print("\nStereoexpansion errors:")
    automech.display_reactions(err_mech)


def prepare_simulation(tag: str, root_path: str | Path) -> None:
    """Read calculation results and prepare simulation.

    :param tag: Mechanism tag
    :param root_path: Project root directory
    """
    # Read mechanisms
    print("\nReading mechanisms...")
    par_mech = automech.io.read(p_.parent_mechanism("json", path=p_.data(root_path)))
    sub_mech = automech.io.read(p_.mechanism(tag, "json", path=p_.data(root_path)))

    # Add calculated thermo to mechanism object
    print("\nAdding calculated thermo...")
    ckin_path = p_.ckin(root_path, tag)
    *_, therm_file = ckin_path.glob("all_therm.ckin*")
    cal_sub_mech = automech.io.chemkin.update.thermo(sub_mech, therm_file)

    # Add calculated rates to mechanism object (use units of parent)
    print("\nAdding calculated rates...")
    rate_files = list(ckin_path.glob("*.ckin"))
    cal_sub_mech = automech.io.chemkin.update.rates(cal_sub_mech, rate_files)

    # Merge updated rates and thermo into parent mechanism
    print("\nExpanding and updating parent...")
    con_mech = automech.expand_parent_stereo(par_mech, cal_sub_mech)
    cal_mech = automech.update(con_mech, cal_sub_mech)

    # Write
    print("\nWriting mechanism to JSON...")
    automech.io.write(
        cal_sub_mech, p_.calculated_mechanism(tag, "json", path=p_.data(root_path))
    )
    automech.io.write(
        con_mech, p_.full_control_mechanism(tag, "json", path=p_.data(root_path))
    )
    automech.io.write(
        cal_mech, p_.full_calculated_mechanism(tag, "json", path=p_.data(root_path))
    )

    print("\nWriting mechanism to Chemkin...")
    con_path = p_.full_control_mechanism(tag, "dat", path=p_.chemkin(root_path))
    print(f"Control: {con_path}")
    automech.io.chemkin.write.mechanism(con_mech, con_path)
    cal_path = p_.full_calculated_mechanism(tag, "dat", path=p_.chemkin(root_path))
    print(f"Calculated: {cal_path}")
    automech.io.chemkin.write.mechanism(cal_mech, cal_path)

    print("\nConverting ChemKin mechanism to Cantera YAML...")
    Parser.convert_mech(
        con_path,
        out_name=p_.full_control_mechanism(tag, "yaml", path=p_.cantera(root_path)),
    )
    Parser.convert_mech(
        cal_path,
        out_name=p_.full_calculated_mechanism(tag, "yaml", path=p_.cantera(root_path)),
    )

    print("\nValidating Cantera model...")
    cantera.Solution(
        p_.full_calculated_mechanism(tag, "yaml", path=p_.cantera(root_path))
    )


def plot_rates(tag: str, root_path: str | Path) -> None:
    """Plot calculated rates.

    :param tag: Mechanism tag
    :param root_path: Project root directory
    """
    # Read mechanisms
    print("\nReading mechanisms...")
    par_mech = automech.io.read(p_.parent_mechanism("json", path=p_.data(root_path)))
    cal_sub_mech = automech.io.read(
        p_.calculated_mechanism(tag, "json", path=p_.data(root_path))
    )

    # Compare calculated to parent mechanism
    print("\nCompare calculated mechanism to parent mechanism...")
    tags0 = previous_tags(tag)
    cal_paths0 = [
        p_.calculated_mechanism(t, "json", path=p_.data(root_path)) for t in tags0
    ]
    cal_mechs0 = list(map(automech.io.read, cal_paths0))
    trues = [True] * len(tags0)
    automech.display_reactions(
        cal_sub_mech,
        comp_mechs=[par_mech, *cal_mechs0],
        comp_labels=["Hill", *tags0],
        comp_stereo=[False, *trues],
    )


def prepare_simulation_species(tag: str, root_path: str | Path) -> None:
    """Simulate model (JSR).

    :param tag: Mechanism tag
    :param root_path: Project root directory
    """
    data_path = p_.data(root_path)
    mech = automech.io.read(p_.full_calculated_mechanism(tag, "json", path=data_path))

    # Read in data and rename species to match simulation
    print("\nReading in species...")
    name_df0 = polars.read_csv(data_path / "hill" / "species.csv")

    # Form join columns with original (stereo-free) names
    tmp_col = c_.temp()
    name_col = Species.name
    name_col0 = c_.orig(name_col)
    name_df0 = name_df0.with_columns(polars.col(name_col0).alias(tmp_col))
    name_df = mech.species.with_columns(
        polars.col(name_col0).fill_null(polars.col(name_col)).alias(tmp_col)
    ).select(name_col, tmp_col)

    # Join to add updated names
    name_df = name_df0.join(name_df, on=tmp_col, how="left").drop(tmp_col)
    assert name_df.select(name_col).null_count().item() == 0

    # Write names to CSV
    print("\nWriting simulation species names to CSV...")
    name_path = p_.simulation_species(tag, path=p_.cantera(root_path))
    print(name_path)
    name_df.write_csv(name_path)
    return name_df


def simulate(
    tag: str,
    root_path: str | Path,
    temp_k: Number = 825,
    pres_atm: Number = 1.1,
    tau_s: Number = 4,
    vol_cm3: Number = 1,
    gather_every: int = 10,
    max_time: int = 180,
) -> None:
    """Simulate model (JSR).

    :param tag: Mechanism tag
    :param root_path: Project root directory
    :param temp_k: Temperature in K
    :param pres_atm: Pressure in atm
    :param tau_s: Residence time in s
    :param vol_cm3: Volume in cm^3
    :param gather_every: Gather every nth point
    :param max_time: Time limit per simulation
    """
    data_path = p_.data(root_path)

    # Read in data and rename species to match simulation
    print("\nReading in species...")
    name_col = Species.name
    name_col0 = c_.orig(name_col)
    name_df0 = polars.read_csv(data_path / "hill" / "species.csv")
    name_df = prepare_simulation_species(tag, root_path)

    # Read in concentration data
    print("\nReading in concentrations...")
    conc_df = polars.read_csv(data_path / "hill" / "concentration.csv")
    conc_df = conc_df.gather_every(gather_every)
    print(conc_df)

    # Determine concentrations for each point
    print("\nDetermining concentrations for each point...")
    spc_dct = dict(name_df0.select("concentration", name_col0).drop_nulls().iter_rows())
    concs = conc_df.rename(spc_dct).select("CPT(563)", "N2", "O2(6)").rows(named=True)
    print(concs)

    # Load mechanism and set initial conditions
    print("\nDefining model and conditions...")
    model = cantera.Solution(
        p_.full_calculated_mechanism(tag, "yaml", path=p_.cantera(root_path))
    )
    model0 = cantera.Solution(
        p_.full_control_mechanism(tag, "yaml", path=p_.cantera(root_path))
    )
    pres_atm *= cantera.one_atm  # convert to Pa from atm
    vol_cm3 *= (1e-2) ** 3  # convert to m^3 from cm^3

    # Run simulations for each point and store the results in an array
    print("\nRunning simulations...")
    sim_dct0 = sim_dct = {s: () for s in name_df[name_col]}
    for conc in concs:
        print(f"Starting simulation for {conc}")
        time0 = time.time()
        try:
            reactor = timeout(reactors.jsr, max_time)(
                model=model,
                temp=temp_k,
                pres=pres_atm,
                tau=tau_s,
                vol=vol_cm3,
                conc=conc,
            )
            x_dct = reactor.thermo.mole_fraction_dict()
            sim_dct = {s: (*x, x_dct.get(s)) for s, x in sim_dct.items()}
            print(f"Calculated: Finished in {time.time() - time0} s")
        except TimeoutError:
            sim_dct = {s: (*x, None) for s, x in sim_dct.items()}
            print(f"Calculated: Timed out after {time.time() - time0} s")

        time0 = time.time()
        try:
            reactor0 = timeout(reactors.jsr, max_time)(
                model=model0,
                temp=temp_k,
                pres=pres_atm,
                tau=tau_s,
                vol=vol_cm3,
                conc=conc,
            )
            x_dct0 = reactor0.thermo.mole_fraction_dict()
            sim_dct0 = {s: (*x, x_dct0[s]) for s, x in sim_dct0.items()}
            print(f"Control: Finished in {time.time() - time0} s")
        except TimeoutError:
            sim_dct0 = {s: (*x, None) for s, x in sim_dct0.items()}
            print(f"Control: Timed out after {time.time() - time0} s")

    print("\nExtracting results...")
    sim_df = conc_df.with_columns(
        polars.Series(s, xs) * 10**6 for s, xs in sim_dct.items()
    )
    print(sim_df)
    sim_df0 = conc_df.with_columns(
        polars.Series(s, xs) * 10**6 for s, xs in sim_dct0.items()
    )
    print(sim_df0)

    print("\nWriting results to CSV...")
    sim_path = p_.full_calculated_mechanism(tag, "csv", path=p_.cantera(root_path))
    print(sim_path)
    sim_df.write_csv(sim_path)
    sim_path0 = p_.full_control_mechanism(tag, "csv", path=p_.cantera(root_path))
    print(sim_path0)
    sim_df0.write_csv(sim_path0)


def plot_simulation(
    tag: str,
    root_path: str | Path,
    x_col: str,
    x_title: str = "O₂ (molec/cm³) ⋅ 10⁻¹⁸",
    y_title: str = "concentration (ppm)",
    control: bool = True,
    line_source_: str | Sequence[str] | None = None,
    point_source: str | None = None,
    my_work_label: str = "This work",
    control_label: str = "Control",
) -> dict[str, altair.Chart]:
    """Plot simulation results.

    :param tag: Mechanism tag
    :param root_path: Project root directory
    :param control: Whether to include the control line
    :param line_source_: Extra data source(s) to plot as line(s)
    :param point_source: Extra data source to plot as points
    :return: Altair chart
    """
    line_source_ = [] if line_source_ is None else line_source_
    line_sources = [line_source_] if isinstance(line_source_, str) else line_source_
    sources = [*line_sources, point_source] if point_source else line_sources

    # Read in simulation results
    name_df = polars.read_csv(p_.simulation_species(tag, path=p_.cantera(root_path)))
    name_df = name_df.filter(polars.col("Experiment").is_not_null())

    sim_df = polars.read_csv(
        p_.full_calculated_mechanism(tag, "csv", path=p_.cantera(root_path))
    )
    sim_df0 = polars.read_csv(
        p_.full_control_mechanism(tag, "csv", path=p_.cantera(root_path))
    )

    data_path = p_.data(root_path)
    data_dct = {s: polars.read_csv(data_path / "hill" / f"{s}.csv") for s in sources}
    data_dct = {s: rename_columns(s, d, name_df) for s, d in data_dct.items()}
    data_dct[my_work_label] = sim_df
    line_sources.insert(0, my_work_label)

    # Add the control line, if requested
    if control:
        data_dct[control_label] = sim_df0
        line_sources.append(control_label)

    chart_dct = {
        name: make_chart(
            data_dct,
            x_col,
            name,
            line_sources=line_sources,
            point_source=point_source,
            x_title=x_title,
            y_title=y_title,
        )
        for name in name_df.get_column(Species.name).to_list()
    }
    return chart_dct


def rename_columns(
    source: str, data_df: polars.DataFrame, name_df: polars.DataFrame
) -> polars.DataFrame:
    """Preprocess data for plotting.

    :param source: Data source
    :param data_df: Simulation data
    :param name_df: Species names
    :return: Preprocessed data
    """
    col_dct = dict(name_df.select(source, Species.name).drop_nulls().iter_rows())
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


COLOR_SEQUENCE = [
    "#ff0000",  # red
    "#0066ff",  # blue
    "#1ab73a",  # green
    "#ef7810",  # orange
    "#8533ff",  # purple
    "#d0009a",  # pink
    "#ffcd00",  # yellow
    "#916e6e",  # brown
]


def make_chart(
    data_dct: dict[str, polars.DataFrame],
    x_col: str,
    y_col: str,
    line_sources: Sequence[str],
    point_source: str | None = None,
    x_title: str | None = None,
    y_title: str | None = None,
) -> altair.Chart:
    """Make an altair chart for one variable.

    :param data_dct: Data sources
    :param x_col: X-axis column
    :param y_col: Y-axis column
    :param line_sources: Data sources to plot as lines
    :param point_source: Extra data source to plot as points
    :return: Joined data
    """
    x_title = x_title or x_col
    y_title = y_title or y_col
    line_dfs = [
        isolate_xy_columns(s, data_dct.get(s), x_col, y_col) for s in line_sources
    ]
    point_df = isolate_xy_columns(
        point_source, data_dct.get(point_source), x_col, y_col
    )

    line_df = functools.reduce(lambda x, y: x.join(y, on=x_col), line_dfs)

    line_colors = altair.Scale(
        domain=line_sources, range=COLOR_SEQUENCE[: len(line_sources)]
    )

    point_chart = (
        altair.Chart(point_df)
        .mark_circle()
        .encode(x=x_col, y=point_source, color=altair.value("black"))
    )
    line_chart = (
        altair.Chart(line_df)
        .mark_line()
        .transform_fold(fold=line_sources)
        .encode(
            x=altair.Y(x_col, title=x_title),
            y=altair.Y("value:Q", title=y_title),
            color=altair.Color("key:N", scale=line_colors),
        )
    )
    return line_chart + point_chart


# Helpers
def timeout(func, seconds=10):
    def raise_timeout_error(signum, frame):
        raise TimeoutError()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        signal.signal(signal.SIGALRM, raise_timeout_error)
        signal.alarm(seconds)
        try:
            result = func(*args, **kwargs)
        finally:
            signal.alarm(0)
        return result

    return wrapper
