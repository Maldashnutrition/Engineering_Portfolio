# Sales Forecasting & BI Dashboard

A data science project for analyzing sales data and forecasting revenue trends. This project combines time‑series analysis with an interactive Streamlit dashboard for business intelligence reporting.

---

## Overview

This project connects to the `sales.db` database and provides:

- **Revenue analysis** – Monthly trends, product performance, and weekly patterns.
- **Time‑series forecasting** – Predict future revenue using Prophet.
- **Interactive dashboard** – Explore data with filters and visualizations.
- **Insight generation** – Identify top products, seasonal patterns, and trends.

### Key Features

- **Data loading** – Connect to SQLite and load sales data with dimensions.
- **Time‑series analysis** – Trend detection, seasonality, moving averages.
- **Forecasting** – 90‑day revenue forecast using Prophet (optional).
- **Interactive dashboard** – Streamlit app for data exploration.
- **Static visualizations** – Publication‑quality charts for reports.

---

## Installation

1. Ensure you have Python 3.8+ and `pip` installed.
2. Copy `sales.db` from the database project into this directory.
3. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
