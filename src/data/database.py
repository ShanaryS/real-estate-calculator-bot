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
                          amortization_data: dict
                          ) -> None:
    """Adds data to amortization table"""

    values = list(amortization_data.values())

    with con:
        for index in range(len(values[0])):
            temp = (values[0][index],
                    values[1][index],
                    values[2][index],
                    values[3][index],
                    values[4][index])

            cur.execute("INSERT INTO [Amortization Table] values (?,?,?,?,?)",
                        temp
                        )


def get_amortization_table(con: sqlite3.dbapi2.Connection
                           ) -> pd.DataFrame:
    """Gets the data from the amortization table"""
    return pd.read_sql_query("SELECT * FROM [Amortization Table]", con,
                             index_col='Period')
