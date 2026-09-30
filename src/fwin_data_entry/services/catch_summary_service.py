"""Catch summary services."""

from fwin_data_entry.database.connection import get_connection
from fwin_data_entry.models.catch_summary import CatchSummary


def create_catch_summary(
    db_path: str,
    catch_summary: CatchSummary,
) -> None:
    """Insert an FN123 record."""

    with get_connection(db_path) as conn:
        conn.execute(
            """
            INSERT INTO FN123 (
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                CATCNT,
                BIOCNT
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                catch_summary.prj_cd,
                catch_summary.sam,
                catch_summary.eff,
                catch_summary.spc,
                catch_summary.catcnt,
                catch_summary.biocnt,
            ),
        )

        conn.commit()


def get_catch_summary(
    db_path: str,
    prj_cd: str,
    sam: int,
    eff: int,
    spc: int,
):
    """Retrieve an FN123 record."""

    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            SELECT *
            FROM FN123
            WHERE PRJ_CD = ?
              AND SAM = ?
              AND EFF = ?
              AND SPC = ?
            """,
            (
                prj_cd,
                sam,
                eff,
                spc,
            ),
        )

        return cursor.fetchone()