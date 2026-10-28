"""Effort services."""

from fwin_data_entry.database.connection import get_connection
from fwin_data_entry.models.effort import Effort
from fwin_data_entry.services.validation import (
    validate_non_negative,
    validate_positive_integer,
    validate_required,
)


def create_effort(
    db_path: str,
    effort: Effort,
) -> None:
    """Insert an effort record."""
    
    validate_required(effort.prj_cd, "PRJ_CD")
    validate_required(effort.gr, "GR")
    validate_required(effort.area, "AREA")
    validate_positive_integer(effort.sam, "SAM")
    validate_non_negative(
        effort.sitem0,
        "SITEM0",
    )

    validate_non_negative(
        effort.secchi,
        "SECCHI",
    )

    validate_non_negative(
        effort.grdepmin,
        "GRDEPMIN",
    )

    validate_non_negative(
        effort.grdepmax,
        "GRDEPMAX",
    )
    
    if (
            effort.grdepmin is not None
        and effort.grdepmax is not None
        and effort.grdepmax < effort.grdepmin
    ):
        raise ValueError(
            "GRDEPMAX must be greater than or equal to GRDEPMIN."
        )

    with get_connection(db_path) as conn:
        conn.execute(
            """
            INSERT INTO FN121 (
                PRJ_CD,
                SAM,
                GR,
                AREA,
                EFF,
                EFFDT0,
                EFFTM0,
                SITEM0,
                DD_LON0,
                DD_LAT0,
                SECCHI,
                GRDEPMIN,
                GRDEPMAX,
                EFFDT1,
                EFFTM1,
                EFFST,
                COMMENT,
                CREW
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                effort.prj_cd,
                effort.sam,
                effort.gr,
                effort.area,
                effort.eff,
                effort.effdt0,
                effort.efftm0,
                effort.sitem0,
                effort.dd_lon0,
                effort.dd_lat0,
                effort.secchi,
                effort.grdepmin,
                effort.grdepmax,
                effort.effdt1,
                effort.efftm1,
                effort.effst,
                effort.comment,
                effort.crew,
            ),
        )

        conn.commit()


def get_effort(
    db_path: str,
    prj_cd: str,
    sam: int,
) -> Effort | None:
    """Retrieve an effort record."""

    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            SELECT *
            FROM FN121
            WHERE PRJ_CD = ?
              AND SAM = ?
            """,
            (
                prj_cd,
                sam,
            ),
        )

        row = cursor.fetchone()

    if row is None:
        return None

    return Effort(
        prj_cd=row[0],
        sam=row[1],
        eff=row[2],
        gr=row[3],
        area=row[4],
        effdt0=row[5],
        efftm0=row[6],
        sitem0=row[7],
        dd_lon0=row[8],
        dd_lat0=row[9],
        secchi=row[10],
        grdepmin=row[11],
        grdepmax=row[12],
        effdt1=row[13],
        efftm1=row[14],
        effst=row[15],
        comment=row[16],
        crew=row[17],
    )
    
def get_next_sam(
    db_path: str,
    prj_cd: str,
) -> int:
    """Return the next available SAM value."""

    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            SELECT MAX(SAM)
            FROM FN121
            WHERE PRJ_CD = ?
            """,
            (prj_cd,),
        )

        result = cursor.fetchone()[0]

    if result is None:
        return 1

    return result + 1

def update_effort(
    db_path: str,
    effort: Effort,
) -> None:
    """Update an FN121 record."""
    validate_non_negative(
        effort.sitem0,
        "SITEM0",
    )

    validate_non_negative(
        effort.secchi,
        "SECCHI",
    )

    validate_non_negative(
        effort.grdepmin,
        "GRDEPMIN",
    )

    validate_non_negative(
        effort.grdepmax,
        "GRDEPMAX",
    )

    if (
        effort.grdepmin is not None
        and effort.grdepmax is not None
        and effort.grdepmax < effort.grdepmin
    ):
        raise ValueError(
            "GRDEPMAX must be greater than or equal to GRDEPMIN."
        )
    with get_connection(db_path) as conn:

        conn.execute(
            """
            UPDATE FN121
            SET
                GR = ?,
                AREA = ?,
                EFFDT0 = ?,
                EFFTM0 = ?,
                SITEM0 = ?,
                DD_LAT0 = ?,
                DD_LON0 = ?,
                SECCHI = ?,
                GRDEPMIN = ?,
                GRDEPMAX = ?,
                EFFDT1 = ?,
                EFFTM1 = ?,
                EFFST = ?,
                CREW = ?,
                COMMENT = ?
            WHERE
                PRJ_CD = ?
                AND SAM = ?
            """,
            (
                effort.gr,
                effort.area,
                effort.effdt0,
                effort.efftm0,
                effort.sitem0,
                effort.dd_lat0,
                effort.dd_lon0,
                effort.secchi,
                effort.grdepmin,
                effort.grdepmax,
                effort.effdt1,
                effort.efftm1,
                effort.effst,
                effort.crew,
                effort.comment,
                effort.prj_cd,
                effort.sam,
            ),
        )

        conn.commit()

def delete_sample(
    db_path: str,
    prj_cd: str,
    sam: int,
) -> None:
    """Delete an FN121 record."""

    with get_connection(db_path) as conn:

        conn.execute(
            """
            DELETE FROM FN121
            WHERE
                PRJ_CD = ?
                AND SAM = ?
            """,
            (
                prj_cd,
                sam,
            ),
        )

        conn.commit()