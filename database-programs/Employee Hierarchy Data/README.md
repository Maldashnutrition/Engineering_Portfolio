# Employee Hierarchy Data

A SQL database project that models an organizational hierarchy using recursive CTEs. This project demonstrates tree traversal, depth calculation, and aggregate queries on hierarchical data – all in SQLite.

---

## Overview

This system manages employee reporting relationships:

- **Employees** – Track employees by name, job title, department, manager, hire date, and salary.
- **Hierarchy** – Self-referencing `manager_id` foreign key creates a tree structure.
- **Recursive Queries** – Traverse the org chart to find subordinates, reporting chains, and subtree aggregates.

### Key Features

- **Self-referencing foreign key** for hierarchical data
- **Recursive CTEs** (`WITH RECURSIVE`) for tree traversal
- **Views** for employee details with manager names
- **Analytical queries** for depth, subtree aggregates, and cycle detection

---

## Schema

The database consists of a single core table:

| Table | Purpose |
|-------|---------|
| `employees` | Employee metadata with `manager_id` self-reference |

---

## Installation

1. Ensure you have SQLite 3.x and Python 3.6+ installed.
2. Copy `employees.db` (or create it via `make init` and `make seed`).
3. Python wrapper uses only the standard library – no external dependencies.

---

## Usage

### Initialize the Database

```bash
make init
