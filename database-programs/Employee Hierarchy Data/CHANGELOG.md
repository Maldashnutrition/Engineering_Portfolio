# Changelog for Employee Hierarchy Data

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

- **Employee Hierarchy Data** – SQL database modeling an organizational hierarchy with recursive CTEs.

  **Schema**:
  - `employees` – Self‑referencing table with `manager_id` foreign key
  - Indexes on `manager_id`, `department`, `hire_date`
  - View `v_employee_with_manager` – Employee details with manager name

  **Recursive CTE Queries**:
  - All subordinates (direct and indirect) of a manager
  - Full reporting chain (path to CEO)
  - Org tree depth for each employee
  - Subtree aggregates (total salary and headcount)
  - Cycle detection
  - Visual tree with indentation

  **Analytical Queries**:
  - Direct reports of a specific manager
  - Average salary by department (with hierarchy depth)
  - Employees with no direct reports (leaves)
  - Most similar employees (by department and salary)

  **CLI Wrapper** (`ini.py`):
  - `make init` – Create database schema
  - `make seed` – Load sample data
  - `make reset` – Delete and recreate database
  - `make query SQL="..."` – Run custom SQL queries
  - `make interactive` – Interactive SQL shell
  - `make all` – Run all pre‑defined analytical queries
  - `make list` – List all available queries

  **Sample Data**:
  - 22 employees across 4 departments (Executive, Engineering, Finance, Operations)
  - Hierarchical depth up to 3 levels
  - Realistic salary and job title data

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
