# Changelog for Library Management System Dashboard

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

- **Library Management System Dashboard** – EDA and visualization project for library data.

  **Data Loading**:
  - Connect to `library.db` using `sqlite3`
  - Load `books`, `members`, `loans`, and `fines` tables
  - Merge tables for combined analysis

  **Visualizations**:
  - Monthly loan trends (line chart)
  - Most borrowed books (bar chart)
  - Genre distribution (pie chart)
  - Member status (active vs inactive)
  - Overdue rate by month (bar chart)
  - Fines distribution (histogram)
  - Membership type breakdown (bar chart)

  **Summary Statistics**:
  - Total books, members, loans, fines
  - Active members count
  - Overdue loans count
  - Most popular genre
  - Most borrowed book

  **Technical Implementation**:
  - Python 3.8+ compatible
  - Modular code: `db_loader.py`, `visualizer.py`
  - Uses `pandas`, `numpy`, `matplotlib`, `seaborn`
  - Makefile for automation: `install`, `run`, `clean`

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
