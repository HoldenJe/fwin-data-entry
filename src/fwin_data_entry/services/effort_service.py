"""Effort services."""

from fwin_data_entry.database.connection import get_connection
from fwin_data_entry.models.effort import Effort


def create_effort(
    db_path: str,
    effort: Effort,
) -> None:
    """Insert an effort record."""

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
):
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

        return cursor.fetchone()