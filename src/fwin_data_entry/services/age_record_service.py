"""Age record services."""

from fwin_data_entry.database.connection import (
    get_connection,
)


def delete_age_records_for_fish(
    db_path: str,
    prj_cd: str,
    sam: int,
    eff: int,
    spc: str,
    fish: int,
) -> None:
    """Delete all FN127 records for a fish."""

    with get_connection(db_path) as conn:

        conn.execute(
            """
            DELETE FROM FN127
            WHERE
                PRJ_CD = ?
                AND SAM = ?
                AND EFF = ?
                AND SPC = ?
                AND FISH = ?
            """,
            (
                prj_cd,
                sam,
                eff,
                spc,
                fish,
            ),
        )

        conn.commit()