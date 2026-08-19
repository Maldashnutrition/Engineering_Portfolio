# Changelog for Sales Analytics

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

- **Sales Analytics** – Star schema data warehouse for sales performance tracking.

  **Schema**:
  - `dim_date` – Date dimension with year, quarter, month, weekday, weekend flag
  - `dim_product` – Product dimension with category, subcategory, brand
  - `dim_store` – Store dimension with location, city, state, region
  - `dim_customer` – Customer dimension with demographics and membership level
  - `sales` – Fact table with quantity, unit_price, discount, revenue

  **Views**:
  - `v_sales_full` – Denormalized sales data with all dimension attributes

  **Analytical Queries**:
  - Monthly revenue trends
  - Top 5 products by revenue
  - 3‑month rolling average
  - Sales by region and category
  - Top 10 customers by revenue
  - Month‑over‑month percentage change
  - Year‑over‑year quarterly comparison
  - Customer lifetime value by membership level
  - Daily cumulative revenue
  - Weekend vs. weekday sales analysis
  - Product popularity by customer age group
  - Discount impact analysis
  - Category contribution to total revenue

  **Window Functions Used**:
  - `LAG` / `LEAD` for time‑series comparisons
  - `RANK` for region‑based product ranking
  - `ROW_NUMBER` for ordering
  - `AVG(...) OVER` for moving averages

  **CLI Wrapper** (`ini.py`):
  - `make init` – Create database schema
  - `make seed` – Load sample data (generated dates and sales)
  - `make reset` – Delete and recreate database
  - `make query SQL="..."` – Run custom SQL queries
  - `make interactive` – Interactive SQL shell
  - `make all` – Run all pre‑defined analytical queries
  - `make list` – List all available queries

  **Sample Data**:
  - 3 years of dates (2023–2025) with full date attributes
  - 20 products across Electronics, Furniture, and Apparel
  - 8 stores across US regions
  - 10 customers with varied demographics
  - 50+ sales transactions

### Fixed

- N/A (initial release)

### Security

- Foreign key constraints maintain referential integrity
- CHECK constraints validate data
- Parameterized queries prevent SQL injection
- No authentication required (local use only)

---

## [0.1.0] – 2026-08-15

### Added

- Initial prototype (not publicly released)

---

[1.0.0]: https://github.com/[your-username]/[repo-name]/releases/tag/v1.0.0
