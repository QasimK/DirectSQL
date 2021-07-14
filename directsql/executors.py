"""Sample backends for executing SQL.

If an executor is missing or incomplete in some way, either send a pull request
or write your own executor from scratch possibly using one of these as a base.
"""
import sqlite3


def sqlite3_executor(file: str, num_statements: int):
    connection = sqlite3.connect(
        file,
        cached_statements=num_statements,
        # Use SQLite's default autocommit mode
        isolation_level=None,
    )

    # Enable name-based access on top of index-based access to rows
    connection.row_factory = sqlite3.Row

    # Enable foreign key constraints
    # Enable sensible, modern performance optimisations
    # See docs/sqlite.md for further details
    connection.executescript(
        """
        PRAGMA foreign_keys = on;
        PRAGMA journal_mode = wal;
        PRAGMA synchronous = normal;
        PRAGMA temp_store = memory;
        PRAGMA mmap_size = 268435456;
        PRAGMA threads = 4;
        PRAGMA secure_delete = on;
    """
    )

    def executor(sql: str, params: dict) -> bytes:
        return connection.execute(sql, params).fetchall()

    # TODO: run pragma optimize; on connection close

    return executor
