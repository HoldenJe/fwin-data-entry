"""Catch summary services."""

from fwin_data_entry.database.connection import get_connection
from fwin_data_entry.models.catch_summary import CatchSummary
from fwin_data_entry.services.validation import (
    validate_required,
    validate_positive_integer,
    validate_non_negative_integer,
    validate_biocnt,
)

def create_catch_summary(
    db_path: str,
    catch_summary: CatchSummary,
) -> None:
    """Insert an FN123 record."""
    validate_required(catch_summary.prj_cd, "PRJ_CD")

    validate_positive_integer(catch_summary.sam, "SAM")
    validate_positive_integer(catch_summary.eff, "EFF")
    validate_positive_integer(catch_summary.spc, "SPC")

    validate_non_negative_integer(
        catch_summary.catcnt,
        "CATCNT",
    )

    validate_non_negative_integer(
        catch_summary.biocnt,
        "BIOCNT",
    )

    validate_biocnt(
        catch_summary.catcnt,
        catch_summary.biocnt,
    )
    
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