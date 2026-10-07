"""Workspace services."""

from fwin_data_entry.database.connection import (
    get_connection,
)
from fwin_data_entry.services.effort_service import (
    get_effort,
)


def get_sample_details(
    db_path: str,
    prj_cd: str,
    sam: int,
):
    """Return the FN121 record for a sample."""

    return get_effort(
        db_path,
        prj_cd,
        sam,
    )

def get_project_samples(
    db_path: str,
):
    """Return all SAM values."""

    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            SELECT SAM
            FROM FN121
            ORDER BY SAM
            """
        )

        return [
            row[0]
            for row in cursor.fetchall()
        ]

def get_sample_catch_summaries(
    db_path: str,
    sam: int,
):
    """Return FN123 records for a sample."""

    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            SELECT SPC, CATCNT, BIOCNT
            FROM FN123
            WHERE SAM = ?
            ORDER BY SPC
            """,
            (sam,),
        )

        return cursor.fetchall()

def get_sample_fish(
    db_path: str,
    sam: int,
):
    """Return FN125 records for a sample."""

    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            SELECT
                FISH,
                SPC,
                FLEN,
                TLEN,
                RWT
            FROM FN125
            WHERE SAM = ?
            ORDER BY SPC, FISH
            """,
            (sam,),
        )

        return cursor.fetchall()