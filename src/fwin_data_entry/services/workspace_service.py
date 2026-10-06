"""Workspace services."""

from fwin_data_entry.database.connection import (
    get_connection,
)


def get_project_samples(
    db_path: str,
):
    """Return all SAM values."""

    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            SELECT SAM
            FROM FN121
            ORDER BY SAM
            """
        )

        return [
            row[0]
            for row in cursor.fetchall()
        ]