"""Database connection utilities."""

import sqlite3


def get_connection(db_path: str) -> sqlite3.Connection:
    """Return a SQLite connection."""

    return sqlite3.connect(db_path)