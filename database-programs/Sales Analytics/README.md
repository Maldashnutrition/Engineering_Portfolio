# Sales Analytics

A data warehouse project using a star schema for sales performance tracking and business intelligence reporting. This project demonstrates dimensional modeling, window functions, and complex analytical queries – all built on SQLite.

---

## Overview

This system provides a complete data warehouse for sales analytics:

- **Fact Table** – `sales` stores transactional sales data.
- **Dimension Tables** – `dim_date`, `dim_product`, `dim_store`, `dim_customer` for rich analysis.
- **Analytical Queries** – Time‑series, rankings, customer lifetime value, and more.

### Key Features

- **Star schema** design for OLAP (online analytical processing)
- **Date dimension** with year, quarter, month, day, and weekend flags
- **Window functions** (`LAG`, `LEAD`, `RANK`, `ROW_NUMBER`)
- **Time‑series analysis** with moving averages and percentage changes
- **Denormalized view** for simplified reporting

---

## Schema

The database consists of a star schema:

| Table | Type | Purpose |
|-------|------|---------|
| `dim_date` | Dimension | Date attributes (year, quarter, month, day, weekday) |
| `dim_product` | Dimension | Product details (name, category, subcategory, brand, price) |
| `dim_store` | Dimension | Store details (name, location, city, state, region) |
| `dim_customer` | Dimension | Customer details (name, email, location, age, gender, membership) |
| `sales` | Fact | Transaction records (date, product, store, customer, quantity, revenue) |


---

## Installation

1. Ensure you have SQLite 3.x and Python 3.6+ installed.
2. Copy `sales.db` (or create it via `make init` and `make seed`).
3. Python wrapper uses only the standard library – no external dependencies.

---

## Usage

### Initialize the Database

```bash
make init
