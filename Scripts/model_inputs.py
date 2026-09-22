"""Loader for MA_model_inputs.xlsx -- the single input file for the MA building-stock model.

This is the only place that knows the workbook's layout. Both dsm_scenario.py and
material_demand.py import it, so the two scripts cannot drift apart on a shared value.

Usage:
    import model_inputs as mi
    p = mi.params()                  # {'year_start': 1997, 'base_year': 2020, ...}
    occ = mi.occupancy_split()       # {'res': 0.724062, 'com': ..., 'pub': ...}
    struct = mi.structure_split()    # {'LF_wood': 0.5949..., ...}
    pop = mi.population()            # DataFrame: Year, SSP1..SSP5
    gdp = mi.gdp()                   # DataFrame: Year, SSP1..SSP5

Note: building lifetimes (Weibull parameters) are deliberately NOT held here -- they
remain hardcoded in the scripts.
"""
from pathlib import Path

import pandas as pd

# resolve from this file, so the scripts work regardless of the working directory
WORKBOOK = Path(__file__).resolve().parent.parent / 'InputData' / 'MA_model_inputs.xlsx'


def _sheet(name):
    return pd.read_excel(WORKBOOK, sheet_name=name)


def params():
    """Model parameters as a dict, e.g. params()['base_year'] -> 2020."""
    df = _sheet('parameters')
    return dict(zip(df['parameter'], df['value']))


def occupancy_split():
    """Share of floor area by occupancy: {'res': .., 'com': .., 'pub': ..}.

    These sum to ~0.94, not 1.0 -- industrial and agricultural floor area are
    excluded from the model. Derived from HAZUS via Scripts/HAZUS_ratio_occupancy.py.
    """
    df = _sheet('occupancy_split')
    return dict(zip(df['occupancy'], df['weight']))


def structure_split():
    """Share of the existing stock by structural system (LF_wood, Steel, ... MH).

    Derived from HAZUS via Scripts/HAZUS_ratio_type.py.
    """
    df = _sheet('structure_split')
    return dict(zip(df['structure'], df['weight']))


def population():
    """Massachusetts population by year and SSP."""
    return _sheet('final pop data')


def gdp():
    """Massachusetts per-capita GDP by year and SSP."""
    return _sheet('final gdp data')
