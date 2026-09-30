"""Catch summary data model."""

from dataclasses import dataclass


@dataclass
class CatchSummary:
    """Representation of an FN123 record."""

    prj_cd: str
    sam: int
    eff: int
    spc: int

    catcnt: int = 0
    biocnt: int = 0
