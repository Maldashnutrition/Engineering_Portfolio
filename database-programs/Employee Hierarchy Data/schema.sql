-- ============================================================
-- Employee Org Chart – Database Schema
-- SQLite 3.x compatible
-- ============================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- Table: employees
-- ------------------------------------------------------------
CREATE TABLE employees (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    job_title       TEXT NOT NULL,
    department      TEXT NOT NULL,
    manager_id      INTEGER REFERENCES employees(id) ON DELETE SET NULL,
    hire_date       DATE NOT NULL,
    salary          DECIMAL(10,2) NOT NULL CHECK (salary > 0),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Indexes
-- ------------------------------------------------------------
CREATE INDEX idx_employees_manager_id ON employees(manager_id);
CREATE INDEX idx_employees_department ON employees(department);
CREATE INDEX idx_employees_hire_date ON employees(hire_date);

-- ------------------------------------------------------------
-- View: employee with manager name
-- ------------------------------------------------------------
CREATE VIEW v_employee_with_manager AS
SELECT
    e.id,
    e.name,
    e.job_title,
    e.department,
    e.manager_id,
    m.name AS manager_name,
    e.hire_date,
    e.salary
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
