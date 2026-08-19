"""
db_loader.py – Load sales data from sales.db.
"""

import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("sales.db")

def get_connection():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"sales.db not found in {DB_PATH}")
    return sqlite3.connect(str(DB_PATH))

def load_sales_data() -> pd.DataFrame:
    """Load sales fact table joined with date dimension."""
    conn = get_connection()
    query = """
    SELECT
        s.sale_id,
        s.date_id,
        d.full_date,
        d.year,
        d.quarter,
        d.month,
        d.month_name,
        d.day_of_week,
        d.day_name,
        d.is_weekend,
        s.product_id,
        s.store_id,
        s.customer_id,
        s.quantity,
        s.unit_price,
        s.discount,
        s.revenue
    FROM sales s
    JOIN dim_date d ON s.date_id = d.date_id
    """
    try:
        df = pd.read_sql_query(query, conn)
        df['full_date'] = pd.to_datetime(df['full_date'])
        return df
    finally:
        conn.close()

def load_daily_revenue() -> pd.DataFrame:
    """Aggregate revenue by day for forecasting."""
    df = load_sales_data()
    daily = df.groupby('full_date')['revenue'].sum().reset_index()
    daily.columns = ['ds', 'y']
    return daily
