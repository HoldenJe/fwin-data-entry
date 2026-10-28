"""Cascade delete services."""

from fwin_data_entry.database.connection import (
    get_connection,
)


def delete_catch_summary_children(
    db_path: str,
    prj_cd: str,
    sam: int,
    eff: int,
    spc: str,
) -> None:
    """Delete child records for an FN123 record."""

    with get_connection(db_path) as conn:

        conn.execute(
            """
            DELETE FROM FN127
            WHERE
                PRJ_CD = ?
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

        conn.execute(
            """
            DELETE FROM FN125
            WHERE
                PRJ_CD = ?
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

        conn.commit()

def delete_sample_children(
    db_path: str,
    prj_cd: str,
    sam: int,
) -> None:
    """Delete child records for an FN121 sample."""

    with get_connection(db_path) as conn:

        conn.execute(
            """
            DELETE FROM FN127
            WHERE
                PRJ_CD = ?
                AND SAM = ?
            """,
            (
                prj_cd,
                sam,
            ),
        )

        conn.execute(
            """
            DELETE FROM FN125
            WHERE
                PRJ_CD = ?
                AND SAM = ?
            """,
            (
                prj_cd,
                sam,
            ),
        )

        conn.execute(
            """
            DELETE FROM FN123
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