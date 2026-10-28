"""Database initialization utilities."""

import sqlite3
from pathlib import Path

from fwin_data_entry.database.schema import (
    FN011_SQL,
    FN121_SQL,
    FN123_SQL,
    FN125_SQL,
    FN127_SQL,
)


def initialize_database(db_path: str) -> None:
    """Create a new database and all required tables."""

    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute(FN011_SQL)
        cursor.execute(FN121_SQL)
        cursor.execute(FN123_SQL)
        cursor.execute(FN125_SQL)
        cursor.execute(FN127_SQL)

        ensure_fn125_comment_column(conn)
        ensure_fn127_table(conn)

        conn.commit()

    print(f"Database initialized: {db_path}")

def ensure_fn125_comment_column(
    conn: sqlite3.Connection,
) -> None:
    """Add COMMENT column to FN125 if missing."""

    cursor = conn.execute(
        "PRAGMA table_info(FN125)"
    )

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if "COMMENT" not in columns:

        conn.execute(
            """
            ALTER TABLE FN125
            ADD COLUMN COMMENT TEXT
            """
        )

        print(
            "Migrated FN125: added COMMENT column"
        )

def ensure_fn127_table(
    conn: sqlite3.Connection,
) -> None:
    """Create FN127 table if missing."""

    conn.execute(FN127_SQL)