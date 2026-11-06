import duckdb
import marimo as mo


database = mo.notebook_dir() / "database.duckdb"


def ask(sql):
    with duckdb.connect(database, read_only=True) as _con:
        return _con.sql(sql).pl()


# Rebuild from scratch every time.
# Delete the old file first, then create tables and load data inside
# with duckdb.connect(database) as _con:
#    ...
