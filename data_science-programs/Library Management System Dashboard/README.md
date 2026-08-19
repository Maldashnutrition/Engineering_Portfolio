# Library Management System Dashboard

A data analysis dashboard for the Library Management System database. This project performs exploratory data analysis (EDA) on library borrowing patterns, member behavior, and overdue trends using Pandas, Matplotlib, and Seaborn.

---

## Overview

This project connects to the `library.db` database and generates visual insights:

- **Monthly loan trends** – Borrowing patterns over time.
- **Most borrowed books** – Popular titles and authors.
- **Genre distribution** – Borrowing by book genre.
- **Member status** – Active vs. inactive members.
- **Overdue rate** – Percentage of overdue loans by month.
- **Fines distribution** – Amounts and frequency of fines.
- **Membership types** – Distribution of member tiers.

### Key Features

- **Data loading** – Connect to SQLite and load tables into DataFrames.
- **Data cleaning** – Handle missing values, convert date types.
- **Visualization** – Generate publication‑quality charts.
- **Summary statistics** – Key metrics about the library system.

---

## Installation

1. Ensure you have Python 3.8+ and `pip` installed.
2. Copy `library.db` from the database project into this directory.
3. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
