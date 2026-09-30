"""Fish sample data model."""

from dataclasses import dataclass


@dataclass
class FishSample:
    """Representation of an FN125 record."""

    prj_cd: str
    sam: int
    eff: int
    spc: int
    fish: int

    flen: float | None = None
    tlen: float | None = None
    rwt: float | None = None

    sex: int | None = None
    mat: int | None = None

    agest: str = ""
    stom: str = ""
    tax: str = ""

    gonwt: float | None = None
    eviswt: float | None = None

    tissue: str = ""