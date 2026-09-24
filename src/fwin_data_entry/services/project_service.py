"""Project services."""

from fwin_data_entry.database.connection import get_connection


def create_project(
    db_path: str,
    prj_cd: str,
    prj_nm: str,
    wby_nm: str,
    prj_date0: str,
    prj_date1: str,
    comment: str = "",
) -> None:
    """Insert a project into FN011."""

    with get_connection(db_path) as conn:
        conn.execute(
            """
            INSERT INTO FN011 (
                PRJ_CD,
                PRJ_NM,
                WBY_NM,
                PRJ_DATE0,
                PRJ_DATE1,
                COMMENT
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                prj_cd,
                prj_nm,
                wby_nm,
                prj_date0,
                prj_date1,
                comment,
            ),
        )

        conn.commit()


def get_project(db_path: str, prj_cd: str):
    """Retrieve a project record."""

    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            SELECT *
            FROM FN011
            WHERE PRJ_CD = ?
            """,
            (prj_cd,),
        )

        return cursor.fetchone()