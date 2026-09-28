"""Effort data model."""

from dataclasses import dataclass


@dataclass
class Effort:
    """Representation of an FN121 effort record."""

    prj_cd: str
    sam: int

    gr: str
    area: str

    eff: int = 999

    effdt0: str = ""
    efftm0: str = ""

    sitem0: float | None = None

    dd_lon0: float | None = None
    dd_lat0: float | None = None

    secchi: float | None = None

    grdepmin: float | None = None
    grdepmax: float | None = None

    effdt1: str = ""
    efftm1: str = ""

    effst: int | None = None

    comment: str = ""
    crew: str = ""