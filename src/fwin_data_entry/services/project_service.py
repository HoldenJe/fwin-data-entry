"""Project services."""

from fwin_data_entry.database.connection import get_connection
from fwin_data_entry.models.project import Project
from fwin_data_entry.services.validation import validate_required

def create_project(
    db_path: str,
    project: Project,
) -> None:
    """Insert a project into FN011."""
    validate_required(project.prj_cd, "PRJ_CD")
    validate_required(project.prj_nm, "PRJ_NM")
    validate_required(project.wby_nm, "WBY_NM")

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
                project.prj_cd,
                project.prj_nm,
                project.wby_nm,
                project.prj_date0,
                project.prj_date1,
                project.comment,
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