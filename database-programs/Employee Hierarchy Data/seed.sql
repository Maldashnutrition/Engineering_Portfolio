-- ============================================================
-- Employee Org Chart – Sample Data
-- ============================================================

-- Insert CEO (top-level)
INSERT INTO employees (name, job_title, department, manager_id, hire_date, salary) VALUES
    ('Alice Johnson', 'CEO', 'Executive', NULL, '2020-01-15', 250000.00);

-- Executive team (report to CEO)
INSERT INTO employees (name, job_title, department, manager_id, hire_date, salary) VALUES
    ('Bob Smith', 'CTO', 'Engineering', 1, '2020-02-01', 180000.00),
    ('Carol White', 'CFO', 'Finance', 1, '2020-03-01', 175000.00),
    ('Dave Brown', 'COO', 'Operations', 1, '2020-04-01', 170000.00);

-- Engineering team (report to CTO)
INSERT INTO employees (name, job_title, department, manager_id, hire_date, salary) VALUES
    ('Eve Davis', 'Director of Engineering', 'Engineering', 2, '2020-05-01', 140000.00),
    ('Frank Wilson', 'Senior Software Engineer', 'Engineering', 2, '2020-06-01', 120000.00),
    ('Grace Moore', 'Software Engineer', 'Engineering', 5, '2020-07-01', 95000.00),
    ('Henry Taylor', 'Software Engineer', 'Engineering', 5, '2020-08-01', 90000.00),
    ('Ivy Anderson', 'DevOps Engineer', 'Engineering', 2, '2020-09-01', 110000.00),
    ('Jack Thomas', 'QA Engineer', 'Engineering', 5, '2020-10-01', 85000.00);

-- Finance team (report to CFO)
INSERT INTO employees (name, job_title, department, manager_id, hire_date, salary) VALUES
    ('Karen Martinez', 'Director of Finance', 'Finance', 3, '2020-11-01', 135000.00),
    ('Leo Garcia', 'Senior Accountant', 'Finance', 11, '2020-12-01', 105000.00),
    ('Mia Robinson', 'Accountant', 'Finance', 11, '2021-01-01', 85000.00);

-- Operations team (report to COO)
INSERT INTO employees (name, job_title, department, manager_id, hire_date, salary) VALUES
    ('Noah Clark', 'Director of Operations', 'Operations', 4, '2021-02-01', 130000.00),
    ('Olivia Rodriguez', 'Operations Manager', 'Operations', 14, '2021-03-01', 110000.00),
    ('Peter Lewis', 'Supply Chain Analyst', 'Operations', 14, '2021-04-01', 90000.00),
    ('Quinn Walker', 'Logistics Coordinator', 'Operations', 15, '2021-05-01', 75000.00),
    ('Rachel Hall', 'Operations Specialist', 'Operations', 15, '2021-06-01', 70000.00);

-- Additional employees in Engineering (under Director)
INSERT INTO employees (name, job_title, department, manager_id, hire_date, salary) VALUES
    ('Samuel Young', 'Senior Software Engineer', 'Engineering', 5, '2021-07-01', 115000.00),
    ('Tina King', 'Software Engineer', 'Engineering', 5, '2021-08-01', 92000.00),
    ('Uma Scott', 'Junior Software Engineer', 'Engineering', 19, '2021-09-01', 78000.00);

-- One more under CTO: a Principal Engineer
INSERT INTO employees (name, job_title, department, manager_id, hire_date, salary) VALUES
    ('Victor Adams', 'Principal Engineer', 'Engineering', 2, '2021-10-01', 150000.00);
