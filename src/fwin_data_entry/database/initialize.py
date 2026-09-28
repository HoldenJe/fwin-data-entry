"""Database initialization utilities."""

from pathlib import Path
import sqlite3

from fwin_data_entry.database.schema import (
    FN011_SQL,
    FN121_SQL,
    FN123_SQL,
    FN125_SQL,
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

        conn.commit()

    print(f"Database initialized: {db_path}")