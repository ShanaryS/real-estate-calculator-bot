import os.path
import sqlite3
from contextlib import contextmanager


@contextmanager
def amortization_table():
    """Used to close database automatically"""
    con = sqlite3.connect(os.path.join('output', 'analysis.db'))
    try:
        cur = con.cursor()
        yield con, cur
    finally:
        con.close()


def create_amortization_table(con: sqlite3.dbapi2.Connection,
                              cur: sqlite3.dbapi2.Cursor
                              ) -> None:
    """Writes analysis to database"""
    with con:
        cur.execute("""CREATE TABLE IF NOT EXISTS [Amortization Table] (
                        Period integer,
                        Monthly Payment real,
                        Principal Payment real,
                        Interest Payment real,
                        Loan Balance real
                    )""")


def drop_amortization_table(con: sqlite3.dbapi2.Connection,
                            cur: sqlite3.dbapi2.Cursor
                            ) -> None:
    """Deletes amortization table"""
    with con:
        cur.execute("DROP TABLE IF EXISTS [Amortization Table]")


def add_amortization_data(con: sqlite3.dbapi2.Connection,
                          cur: sqlite3.dbapi2.Cursor,
                          amortization_data: dict) -> None:
    """Adds data to amortization table"""

    with con:
        cur.execute("INSERT INTO [Amortization Table] values (?,?,?,?,?)",
                    (amortization_data['Period'],
                     amortization_data['Monthly Payment'],
                     amortization_data['Principal Payment'],
                     amortization_data['Interest Payment'],
                     amortization_data['Loan Balance']
                     )
                    )


def get_amortization_table(cur: sqlite3.dbapi2.Cursor
                           ) -> list:
    """Gets the data from the amortization table"""
    cur.execute("SELECT * FROM [Amortization Table]")
    return cur.fetchall()
