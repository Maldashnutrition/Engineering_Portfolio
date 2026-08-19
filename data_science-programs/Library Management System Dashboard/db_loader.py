"""
db_loader.py – Load data from library.db into Pandas DataFrames.
"""

import sqlite3
import pandas as pd
from pathlib import Path

# Look for library.db in current directory, then in data/ subdir
CANDIDATE_PATHS = [
    Path("library.db"),
    Path("data/library.db"),
]

DB_PATH = None
for p in CANDIDATE_PATHS:
    if p.exists():
        DB_PATH = p
        break

if DB_PATH is None:
    raise FileNotFoundError("library.db not found. Please place it in the current directory or data/ subdirectory.")

def get_connection():
    return sqlite3.connect(str(DB_PATH))

def load_table(table_name: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        return df
    finally:
        conn.close()

def load_books():
    return load_table("books")

def load_members():
    return load_table("members")

def load_loans():
    return load_table("loans")

def load_fines():
    return load_table("fines")

def load_all():
    return {
        "books": load_books(),
        "members": load_members(),
        "loans": load_loans(),
        "fines": load_fines(),
    }
