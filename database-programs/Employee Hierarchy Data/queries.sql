-- ============================================================
-- Employee Org Chart – Analytical Queries
-- ============================================================

-- ------------------------------------------------------------
-- 1. Full org chart (all employees with their manager)
-- ------------------------------------------------------------
SELECT
    e.id,
    e.name,
    e.job_title,
    e.department,
    m.name AS manager_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id
ORDER BY e.id;

-- ------------------------------------------------------------
-- 2. Direct reports of a specific manager (e.g., ID=2 – CTO)
-- ------------------------------------------------------------
SELECT
    id,
    name,
    job_title,
    department
FROM employees
WHERE manager_id = 2
ORDER BY name;

-- ------------------------------------------------------------
-- 3. Recursive CTE: All subordinates (direct and indirect) of a manager
-- ------------------------------------------------------------
WITH RECURSIVE subordinates AS (
    -- Anchor: start with the manager
    SELECT
        id,
        name,
        job_title,
        department,
        0 AS depth
    FROM employees
    WHERE id = 2   -- CTO

    UNION ALL

    -- Recursive: find employees who report to someone already in the set
    SELECT
        e.id,
        e.name,
        e.job_title,
        e.department,
        s.depth + 1
    FROM employees e
    JOIN subordinates s ON e.manager_id = s.id
)
SELECT
    id,
    name,
    job_title,
    department,
    depth
FROM subordinates
ORDER BY depth, name;

-- ------------------------------------------------------------
-- 4. Full reporting path (chain of command) for a given employee
-- ------------------------------------------------------------
WITH RECURSIVE chain AS (
    -- Start with the employee
    SELECT
        id,
        name,
        manager_id,
        0 AS level
    FROM employees
    WHERE id = 19   -- Samuel Young (or any employee)

    UNION ALL

    -- Walk up to the manager
    SELECT
        e.id,
        e.name,
        e.manager_id,
        c.level + 1
    FROM employees e
    JOIN chain c ON e.id = c.manager_id
)
SELECT
    id,
    name,
    level
FROM chain
ORDER BY level DESC;   -- top-level first

-- ------------------------------------------------------------
-- 5. Org tree depth (max depth) and each employee's depth
-- ------------------------------------------------------------
WITH RECURSIVE depth_calc AS (
    SELECT
        id,
        name,
        manager_id,
        0 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT
        e.id,
        e.name,
        e.manager_id,
        d.depth + 1
    FROM employees e
    JOIN depth_calc d ON e.manager_id = d.id
)
SELECT
    id,
    name,
    depth
FROM depth_calc
ORDER BY depth DESC, name;

-- ------------------------------------------------------------
-- 6. Average salary by department (with hierarchy depth)
-- ------------------------------------------------------------
WITH RECURSIVE depth_calc AS (
    SELECT
        id,
        manager_id,
        department,
        0 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT
        e.id,
        e.manager_id,
        e.department,
        d.depth + 1
    FROM employees e
    JOIN depth_calc d ON e.manager_id = d.id
)
SELECT
    e.department,
    COUNT(*) AS employee_count,
    ROUND(AVG(e.salary), 2) AS avg_salary,
    MAX(d.depth) AS max_depth
FROM employees e
JOIN depth_calc d ON e.id = d.id
GROUP BY e.department
ORDER BY avg_salary DESC;

-- ------------------------------------------------------------
-- 7. Find employees with no direct reports (leaves)
-- ------------------------------------------------------------
SELECT
    e.id,
    e.name,
    e.job_title,
    e.department
FROM employees e
LEFT JOIN employees m ON e.id = m.manager_id
WHERE m.id IS NULL
ORDER BY e.name;

-- ------------------------------------------------------------
-- 8. Hierarchy with indentation (visual tree)
-- ------------------------------------------------------------
WITH RECURSIVE tree AS (
    SELECT
        id,
        name,
        job_title,
        manager_id,
        0 AS depth,
        name AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT
        e.id,
        e.name,
        e.job_title,
        e.manager_id,
        t.depth + 1,
        t.path || ' -> ' || e.name
    FROM employees e
    JOIN tree t ON e.manager_id = t.id
)
SELECT
    depth,
    REPLACE(REPLACE(QUOTE(''), '''', ''), '', '') || name AS hierarchy,
    job_title
FROM tree
ORDER BY path;

-- ------------------------------------------------------------
-- 9. Subtree aggregate: total salary and headcount under each manager
-- ------------------------------------------------------------
WITH RECURSIVE subtree AS (
    SELECT
        id,
        manager_id,
        salary,
        1 AS count
    FROM employees

    UNION ALL

    SELECT
        e.id,
        e.manager_id,
        e.salary,
        1
    FROM employees e
    JOIN subtree s ON e.manager_id = s.id
)
SELECT
    e.id AS manager_id,
    e.name AS manager_name,
    SUM(s.salary) AS total_subtree_salary,
    COUNT(s.id) AS total_subtree_count
FROM employees e
JOIN subtree s ON e.id = s.id
GROUP BY e.id, e.name
ORDER BY total_subtree_count DESC;

-- ------------------------------------------------------------
-- 10. Cycle detection (should return empty if no cycles)
-- ------------------------------------------------------------
WITH RECURSIVE cycle_detection AS (
    SELECT
        id,
        name,
        manager_id,
        0 AS level,
        id AS path
    FROM employees
    WHERE manager_id IS NOT NULL

    UNION ALL

    SELECT
        e.id,
        e.name,
        e.manager_id,
        c.level + 1,
        c.path || ',' || e.id
    FROM employees e
    JOIN cycle_detection c ON e.manager_id = c.id
    WHERE INSTR(c.path, ',' || e.id || ',') = 0
)
SELECT * FROM cycle_detection
WHERE level > 0;
