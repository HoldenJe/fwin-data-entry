"""Age record services."""

from fwin_data_entry.database.connection import (
    get_connection,
)
from fwin_data_entry.models.age_record import (
    AgeRecord,
)


def create_age_record(
    db_path: str,
    age_record: AgeRecord,
) -> None:
    """Insert an FN127 record."""

    with get_connection(db_path) as conn:

        conn.execute(
            """
            INSERT INTO FN127 (
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                FISH,
                AGEID,
                AGEMT,
                AGEA,
                NCA,
                EDGE,
                CONF
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                age_record.prj_cd,
                age_record.sam,
                age_record.eff,
                age_record.spc,
                age_record.fish,
                age_record.ageid,
                age_record.agemt,
                age_record.agea,
                age_record.nca,
                age_record.edge,
                age_record.conf,
            ),
        )

        conn.commit()

def get_age_record(
    db_path: str,
    prj_cd: str,
    sam: int,
    eff: int,
    spc: str,
    fish: int,
    ageid: int,
) -> AgeRecord | None:
    """Retrieve an FN127 record."""

    with get_connection(db_path) as conn:

        cursor = conn.execute(
            """
            SELECT
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                FISH,
                AGEID,
                AGEMT,
                AGEA,
                NCA,
                EDGE,
                CONF
            FROM FN127
            WHERE
                PRJ_CD = ?
                AND SAM = ?
                AND EFF = ?
                AND SPC = ?
                AND FISH = ?
                AND AGEID = ?
            """,
            (
                prj_cd,
                sam,
                eff,
                spc,
                fish,
                ageid,
            ),
        )

        row = cursor.fetchone()

    if row is None:
        return None

    return AgeRecord(
        prj_cd=row[0],
        sam=row[1],
        eff=row[2],
        spc=row[3],
        fish=row[4],
        ageid=row[5],
        agemt=row[6],
        agea=row[7],
        nca=row[8],
        edge=row[9],
        conf=row[10],
    )

def get_next_ageid(
    db_path: str,
    prj_cd: str,
    sam: int,
    eff: int,
    spc: str,
    fish: int,
) -> int:
    """Return the next available AGEID."""

    with get_connection(db_path) as conn:

        cursor = conn.execute(
            """
            SELECT MAX(AGEID)
            FROM FN127
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

        result = cursor.fetchone()[0]

    if result is None:
        return 1

    return result + 1

def update_age_record(
    db_path: str,
    age_record: AgeRecord,
) -> None:
    """Update an FN127 record."""

    with get_connection(db_path) as conn:

        conn.execute(
            """
            UPDATE FN127
            SET
                AGEMT = ?,
                AGEA = ?,
                NCA = ?,
                EDGE = ?,
                CONF = ?
            WHERE
                PRJ_CD = ?
                AND SAM = ?
                AND EFF = ?
                AND SPC = ?
                AND FISH = ?
                AND AGEID = ?
            """,
            (
                age_record.agemt,
                age_record.agea,
                age_record.nca,
                age_record.edge,
                age_record.conf,
                age_record.prj_cd,
                age_record.sam,
                age_record.eff,
                age_record.spc,
                age_record.fish,
                age_record.ageid,
            ),
        )

        conn.commit()

def delete_age_record(
    db_path: str,
    prj_cd: str,
    sam: int,
    eff: int,
    spc: str,
    fish: int,
    ageid: int,
) -> None:
    """Delete a single FN127 record."""

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
                AND AGEID = ?
            """,
            (
                prj_cd,
                sam,
                eff,
                spc,
                fish,
                ageid,
            ),
        )

        conn.commit()

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

