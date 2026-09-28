"""Project data model."""

from dataclasses import dataclass


@dataclass
class Project:
    """Representation of an FN011 project record."""

    prj_cd: str
    prj_nm: str
    wby_nm: str
    prj_date0: str
    prj_date1: str
    comment: str = ""