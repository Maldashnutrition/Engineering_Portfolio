# Changelog for Sales Forecasting & BI Dashboard

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned

- None currently.

---

## [1.0.0] – 2026-08-16

### Added

- **Sales Forecasting & BI Dashboard** – Time‑series analysis and forecasting for sales data.

  **Data Loading**:
  - Connect to `sales.db` using `sqlite3`
  - Load sales fact table joined with date dimension
  - Aggregate daily revenue for forecasting

  **Visualizations**:
  - Monthly revenue (bar chart)
  - Top 10 products by revenue (bar chart)
  - Revenue by day of week (bar chart)
  - Daily revenue trend (line chart)
  - Revenue forecast with confidence intervals (line chart)

  **Forecasting**:
  - Prophet model for 90‑day revenue forecast
  - Confidence intervals (95%)
  - Annual and weekly seasonality detection
  - Forecast data exported to CSV

  **Streamlit Dashboard** (`app.py`):
  - Date range filter
  - Key metrics (total revenue, sales count, unique products, customers)
  - Revenue trend chart (Plotly)
  - Forecast execution button
  - Top products bar chart

  **Technical Implementation**:
  - Python 3.8+ compatible
  - Modular code: `db_loader.py`, `visualizer.py`
  - Uses `pandas`, `numpy`, `matplotlib`, `seaborn`, `prophet`, `streamlit`, `plotly`
  - Makefile for automation: `install`, `run`, `dashboard`, `clean`

### Fixed

- N/A (initial release)

### Security

- Read‑only access to database
- No system modifications
- Output written to `output/` folder only

---

## [0.1.0] – 2026-08-15

### Added

- Initial prototype (not publicly released)

---

[1.0.0]: https://github.com/[your-username]/[repo-name]/releases/tag/v1.0.0
