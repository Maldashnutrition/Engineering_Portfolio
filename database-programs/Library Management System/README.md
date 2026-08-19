# Library Management System

A complete SQL database project for managing books, members, loans, and fines. This project demonstrates database schema design, triggers, views, indexes, and complex analytical queries – all built on SQLite.

---

## Overview

This system manages a library's core operations:

- **Books** – Track books by title, author, ISBN, genre, and copies.
- **Members** – Manage members with different membership types and contact details.
- **Loans** – Record book loans with due dates, return dates, and status tracking.
- **Fines** – Automatically calculate and track fines for overdue loans.

### Key Features

- **Foreign key constraints** for data integrity
- **Triggers** for automatic availability updates and fine generation
- **Views** for active loans, overdue loans, and member history
- **Indexes** for performance optimization
- **Preventative logic** – No loan if no copies are available

---

## Schema

The database consists of four main tables:

| Table | Purpose |
|-------|---------|
| `books` | Book metadata and available copies |
| `members` | Member information and membership type |
| `loans` | Loan records with status and dates |
| `fines` | Fine records with payment status |


## Installation

1. Ensure you have SQLite 3.x and Python 3.6+ installed.
2. Copy `library.db` (or create it via `make init` and `make seed`).
3. Install Python dependencies (if any; the wrapper uses only the standard library).

---

## Usage

### Initialize the Database

```bash
make init
