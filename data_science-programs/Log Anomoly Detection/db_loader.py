"""
db_loader.py – Load log data from logs.db.
"""

import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("logs.db")

def get_connection():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"logs.db not found in {DB_PATH}")
    return sqlite3.connect(str(DB_PATH))

def load_web_logs() -> pd.DataFrame:
    """Load web_logs table."""
    conn = get_connection()
    query = """
    SELECT
        id,
        log_timestamp,
        client_ip,
        method,
        path,
        status_code,
        bytes_sent,
        response_time_ms,
        user_agent,
        referer
    FROM web_logs
    """
    try:
        df = pd.read_sql_query(query, conn)
        df['log_timestamp'] = pd.to_datetime(df['log_timestamp'])
        return df
    finally:
        conn.close()

def load_error_logs() -> pd.DataFrame:
    """Load error_logs table."""
    conn = get_connection()
    query = "SELECT * FROM error_logs"
    try:
        df = pd.read_sql_query(query, conn)
        df['error_timestamp'] = pd.to_datetime(df['error_timestamp'])
        return df
    finally:
        conn.close()
