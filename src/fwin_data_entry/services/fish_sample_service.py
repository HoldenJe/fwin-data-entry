"""Fish sample services."""

from fwin_data_entry.database.connection import get_connection
from fwin_data_entry.models.fish_sample import FishSample


def create_fish_sample(
    db_path: str,
    fish_sample: FishSample,
) -> None:
    """Insert an FN125 record."""

    with get_connection(db_path) as conn:
        conn.execute(
            """
            INSERT INTO FN125 (
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                FISH,
                FLEN,
                TLEN,
                RWT,
                SEX,
                MAT,
                AGEST,
                STOM,
                TAXON,
                GONWT,
                EVISWT,
                TISSUE
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                fish_sample.prj_cd,
                fish_sample.sam,
                fish_sample.eff,
                fish_sample.spc,
                fish_sample.fish,
                fish_sample.flen,
                fish_sample.tlen,
                fish_sample.rwt,
                fish_sample.sex,
                fish_sample.mat,
                fish_sample.agest,
                fish_sample.stom,
                fish_sample.taxon,
                fish_sample.gonwt,
                fish_sample.eviswt,
                fish_sample.tissue,
            ),
        )

        conn.commit()


def get_fish_sample(
    db_path: str,
    prj_cd: str,
    sam: int,
    eff: int,
    spc: int,
    fish: int,
) -> FishSample | None:
    """Retrieve an FN125 record."""

    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            SELECT *
            FROM FN125
            WHERE PRJ_CD = ?
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

        row = cursor.fetchone()

    if row is None:
        return None

    return FishSample(
        prj_cd=row[0],
        sam=row[1],
        eff=row[2],
        spc=row[3],
        fish=row[4],
        flen=row[5],
        tlen=row[6],
        rwt=row[7],
        sex=row[8],
        mat=row[9],
        agest=row[10],
        stom=row[11],
        taxon=row[12],
        gonwt=row[13],
        eviswt=row[14],
        tissue=row[15],
    )
    
def get_next_fish(
    db_path: str,
    prj_cd: str,
    sam: int,
    eff: int,
    spc: int,
) -> int:
    """Return the next available fish number."""

    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            SELECT MAX(FISH)
            FROM FN125
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

        result = cursor.fetchone()[0]

    if result is None:
        return 1

    return result + 1

def update_fish_sample(
    db_path: str,
    fish_sample: FishSample,
) -> None:
    """Update an existing FN125 record."""

    with get_connection(db_path) as conn:

        conn.execute(
            """
            UPDATE FN125
            SET
                FLEN = ?,
                TLEN = ?,
                RWT = ?,
                SEX = ?,
                MAT = ?,
                AGEST = ?,
                STOM = ?,
                TAXON = ?,
                GONWT = ?,
                EVISWT = ?,
                TISSUE = ?
            WHERE
                PRJ_CD = ?
                AND SAM = ?
                AND EFF = ?
                AND SPC = ?
                AND FISH = ?
            """,
            (
                fish_sample.flen,
                fish_sample.tlen,
                fish_sample.rwt,
                fish_sample.sex,
                fish_sample.mat,
                fish_sample.agest,
                fish_sample.stom,
                fish_sample.taxon,
                fish_sample.gonwt,
                fish_sample.eviswt,
                fish_sample.tissue,
                fish_sample.prj_cd,
                fish_sample.sam,
                fish_sample.eff,
                fish_sample.spc,
                fish_sample.fish,
            ),
        )

        conn.commit()