import os.path
import sqlite3
import pandas as pd
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
                          amortization_data: dict, index: int,
                          commit=True) -> None:
    """Adds data to amortization table"""

    if commit:
        with con:
            cur.execute("INSERT INTO [Amortization Table] values (?,?,?,?,?)",
                        (amortization_data['Period'][index],
                         amortization_data['Monthly Payment'][index],
                         amortization_data['Principal Payment'][index],
                         amortization_data['Interest Payment'][index],
                         amortization_data['Loan Balance'][index]
                         )
                        )
    else:
        cur.execute("INSERT INTO [Amortization Table] values (?,?,?,?,?)",
                    (amortization_data['Period'][index],
                     amortization_data['Monthly Payment'][index],
                     amortization_data['Principal Payment'][index],
                     amortization_data['Interest Payment'][index],
                     amortization_data['Loan Balance'][index]
                     )
                    )


def get_amortization_table(cur: sqlite3.dbapi2.Cursor
                           ) -> list:
    """Gets the data from the amortization table"""
    cur.execute("SELECT * FROM [Amortization Table]")
    return cur.fetchall()
