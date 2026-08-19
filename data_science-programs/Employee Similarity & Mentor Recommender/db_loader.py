

import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("employees.db")

def get_connection():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"employees.db not found in {DB_PATH}")
    return sqlite3.connect(str(DB_PATH))

def load_employees() -> pd.DataFrame:
    query = """
    SELECT
        id,
        name,
        job_title,
        department,
        manager_id,
        hire_date,
        salary
    FROM employees
    """
    df = pd.read_sql_query(query, get_connection())
    df['hire_date'] = pd.to_datetime(df['hire_date'])
    return df

def load_managers() -> pd.DataFrame:
    """Load manager names for each employee."""
    query = """
    SELECT
        e.id,
        e.name,
        e.job_title,
        e.department,
        m.name AS manager_name,
        m.job_title AS manager_job_title
    FROM employees e
    LEFT JOIN employees m ON e.manager_id = m.id
    """
    return pd.read_sql_query(query, get_connection())
