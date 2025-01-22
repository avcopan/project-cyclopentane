"""Project workflows."""

from numbers import Number
from pathlib import Path

import polars

import automech
from automech import Mechanism
from automech.schema import Species
from automech.util import col_

from ._util import ckin_path as ckin_path_
from ._util import data_path as data_path_
from .sim import reactors


# Workflows
def write(mech: Mechanism, tag: str, root_path: str | Path) -> None:
    """Write mechanism for calculation.

    :param mech: Mechanism
    :param tag: Mechanism tag
    :param root_path: Project root directory
    """
    data_path = data_path_(root_path)

    # Display
    print("\nFinalizing build for...")
    print(mech)
    automech.display(mech)

    # Expand and sort
    print("\nExpanding stereochemistry...")
    mech, err_mech = automech.expand_stereo(mech, distinct_ts=False)
    mech = automech.with_sort_data(mech)

    # Write
    print("\nWriting mechanism...")
    json_path = data_path / f"{tag}.json"
    reac_path = data_path / "mechanalyzer" / f"{tag}.dat"
    spec_path = data_path / "mechanalyzer" / f"{tag}.csv"
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
    par_mech0 = automech.io.read(data_path / "full_raw.json")
    cal_mech0 = automech.io.read(data_path / f"{tag}.json")

    # Add calculated thermo to mechanism object
    print("\nAdding calculated thermo...")
    *_, therm_file = ckin_path.glob("all_therm.ckin*")
    cal_mech = automech.io.chemkin.update.thermo(cal_mech0, therm_file)

    # Add calculated rates to mechanism object (use units of parent)
    print("\nAdding calculated rates...")
    rate_files = list(ckin_path.glob("*.ckin"))
    cal_mech = automech.set_rate_units(cal_mech, automech.rate_units(par_mech0))
    cal_mech = automech.io.chemkin.update.rates(cal_mech, rate_files)

    # Merge updated rates and thermo into parent mechanism
    print("\nExpanding and updating parent...")
    mech0 = automech.expand_parent_stereo(par_mech0, cal_mech)
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

    # Visualize intersections with the calculated mechanism
    print("\nCompare calculated mechanism to parent mechanism...")
    int_par_mech0 = automech.intersection(par_mech0, cal_mech, stereo=False)
    int_cal_mech = automech.intersection(par_mech0, cal_mech, right=True, stereo=False)
    dif_cal_mech = automech.difference(par_mech0, cal_mech, right=True, stereo=False)
    int_mech = automech.intersection(mech, cal_mech, stereo=False)
    print("\n1. Original (compare):")
    print(automech.io.chemkin.write.reactions_block(int_par_mech0, frame=False))
    print("\n2. Calculated (compare):")
    print(automech.io.chemkin.write.reactions_block(int_cal_mech, frame=False))
    if not automech.reaction_count(dif_cal_mech) == 0:
        print("\n3. Calculated (new):")
        print(automech.io.chemkin.write.reactions_block(dif_cal_mech, frame=False))
        print("\n\n4. Calculated (all together):")
        print(automech.io.chemkin.write.reactions_block(int_mech, frame=False))


def simulate(
    full_tag: str,
    root_path: str | Path,
    temp_k: Number = 825,
    pres_atm: Number = 1.1,
    tau_s: Number = 4,
    vol_cm3: Number = 1,
    gather_every: int = 1,
) -> None:
    """Read calculation results.

    TODO: Run ChemKin -> Cantera conversion

    :param tag: Mechanism tag
    :param root_path: Project root directory
    :param temp_k: Temperature in K
    :param pres_atm: Pressure in atm
    :param tau_s: Residence time in s
    :param vol_cm3: Volume in cm^3
    :param gather_every: Gather every nth point
    """
    import cantera
    from cantera.ck2yaml import Parser

    data_path = data_path_(root_path)

    # Read in data and rename species to match simulation
    print("\nReading in species...")
    spc_df0 = polars.read_csv(data_path / "hill" / "species.csv")
    spc_df = automech.species(automech.io.read(data_path / f"{full_tag}.json"))
    name_col = Species.name
    name_col0 = col_.orig(name_col)
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
