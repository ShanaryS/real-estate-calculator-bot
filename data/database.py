import os.path
import sqlite3


def create_database() -> (sqlite3.dbapi2.Connection, sqlite3.dbapi2.Cursor):
    """Creates the database"""

    con = sqlite3.connect(os.path.join('output', 'analysis.db'))
    cur = con.cursor()

    return con, cur


def write_to_database(cur: sqlite3.dbapi2.Cursor) -> None:
    """Writes analysis to database"""
    cur.execute("create table lang (name, first_appeared)")


def commit_to_database(con: sqlite3.dbapi2.Connection) -> None:
    """Commits changes to database"""
    con.commit()


def close_database(con: sqlite3.dbapi2.Connection) -> None:
    """Closes the database"""
    con.close()
