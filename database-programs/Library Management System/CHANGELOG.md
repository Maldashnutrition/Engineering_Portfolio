# Changelog for Library Management System

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

- **Library Management System** – Complete SQL database for managing books, members, loans, and fines.

  **Schema**:
  - `books` – Book metadata with `copies_total` and `copies_available`
  - `members` – Member information with `membership_type` and `is_active`
  - `loans` – Loan records with `status` tracking (active, returned, overdue)
  - `fines` – Fine records with payment tracking
  - `categories` – Book genre classification

  **Views**:
  - `v_active_loans` – Currently active loans with days remaining
  - `v_overdue_loans` – Overdue loans with calculated fines
  - `v_member_history` – Per‑member borrowing statistics
  - `v_book_popularity` – Per‑book borrow counts

  **Triggers**:
  - `trg_loan_create` – Decreases `copies_available` on loan creation
  - `trg_loan_return` – Increases `copies_available` on return
  - `trg_loan_overdue` – Updates status to `overdue` when due date passes
  - `trg_fine_on_return` – Auto‑generates fines for late returns
  - `trg_prevent_loan_when_no_copies` – Prevents loans when no copies available

  **Indexes**:
  - Performance optimization on `isbn`, `title`, `author`, `email`, `status`, `due_date`, etc.

  **CLI Wrapper** (`ini.py`):
  - `make init` – Create database schema
  - `make seed` – Load sample data
  - `make reset` – Delete and recreate database
  - `make query SQL="..."` – Run custom SQL queries
  - `make interactive` – Interactive SQL shell
  - `make all` – Run all pre‑defined analytical queries
  - `make list` – List all available queries

  **Sample Data**:
  - 20 books across multiple genres
  - 14 members with different membership types
  - 20+ loans (active, returned, overdue)
  - 5 fines (paid and unpaid)

### Fixed

- N/A (initial release)

### Security

- Foreign key constraints maintain referential integrity
- CHECK constraints validate data
- Parameterized queries prevent SQL injection (in Python wrapper)
- No authentication required (local use only)

---

## [0.1.0] – 2026-08-15

### Added

- Initial prototype (not publicly released)

---

[1.0.0]: https://github.com/[your-username]/[repo-name]/releases/tag/v1.0.0
