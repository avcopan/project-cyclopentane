"""Cantera reactors."""

from collections.abc import Mapping
from numbers import Number

import cantera as ct
from cantera import ReactorNet, Solution


def jsr(
    model: Solution,
    temp: Number,
    pres: Number,
    tau: Number,
    vol: Number,
    conc: Mapping[str, Number],
) -> ReactorNet:
    """Run a jet-stirred reactor simulation.

    :param model: Chemical kinetics model
    :param temp: Temperature
    :param pres: Pressure
    :param tau: Residence time
    :param conc: Starting concentrations
    :return: Solved simulation reactor network
    """
    # Use concentrations from the previous iteration to speed up convergence
    model.TPX = temp, pres, conc

    # Set up JSR: inlet -> flow control -> reactor -> pressure control -> exhaust
    reactor = ct.IdealGasReactor(model, energy="off", volume=vol)
    exhaust = ct.Reservoir(model)
    inlet = ct.Reservoir(model)
    ct.PressureController(
        upstream=reactor,
        downstream=exhaust,
        K=1e-3,
        primary=ct.MassFlowController(
            upstream=inlet,
            downstream=reactor,
            mdot=reactor.mass / tau,
        ),
    )
    reactor_net = ct.ReactorNet([reactor])
    reactor_net.advance_to_steady_state()
    return reactor
