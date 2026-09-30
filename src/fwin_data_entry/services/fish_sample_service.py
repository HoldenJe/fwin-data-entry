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
):
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

        return cursor.fetchone()