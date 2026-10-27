"""Age structure data model."""

from dataclasses import dataclass


@dataclass
class AgeRecord:
    """Representation of an FN127 record."""

    prj_cd: str
    sam: int
    eff: int
    spc: str
    fish: int
    ageid: int

    agemt: str = ""
    agea: int | None = None
    nca: int | None = None
    edge: str = ""
    conf: int | None = None