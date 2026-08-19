-- ============================================================
-- Library Management System – Analytical Queries
-- ============================================================

-- ------------------------------------------------------------
-- 1. Find all active loans with member and book details
-- ------------------------------------------------------------
SELECT
    l.id AS loan_id,
    m.name AS member_name,
    m.email AS member_email,
    b.title AS book_title,
    b.author AS book_author,
    l.loan_date,
    l.due_date,
    CASE
        WHEN l.due_date < DATE('now') AND l.return_date IS NULL THEN 'OVERDUE'
        ELSE 'ACTIVE'
    END AS status
FROM loans l
JOIN members m ON l.member_id = m.id
JOIN books b ON l.book_id = b.id
WHERE l.return_date IS NULL
ORDER BY l.due_date ASC;

-- ------------------------------------------------------------
-- 2. Books with no available copies (fully borrowed)
-- ------------------------------------------------------------
SELECT
    title,
    author,
    copies_total,
    copies_available
FROM books
WHERE copies_available = 0;

-- ------------------------------------------------------------
-- 3. Top 10 most borrowed books
-- ------------------------------------------------------------
SELECT
    b.title,
    b.author,
    COUNT(l.id) AS borrow_count
FROM books b
JOIN loans l ON b.id = l.book_id
GROUP BY b.id, b.title, b.author
ORDER BY borrow_count DESC
LIMIT 10;

-- ------------------------------------------------------------
-- 4. Members with outstanding fines
-- ------------------------------------------------------------
SELECT
    m.name,
    m.email,
    SUM(f.amount) AS total_fines_owed
FROM members m
JOIN loans l ON m.id = l.member_id
JOIN fines f ON l.id = f.loan_id
WHERE f.paid = 0
GROUP BY m.id, m.name, m.email
HAVING total_fines_owed > 0
ORDER BY total_fines_owed DESC;

-- ------------------------------------------------------------
-- 5. Books by genre with borrow statistics
-- ------------------------------------------------------------
SELECT
    b.genre,
    COUNT(DISTINCT b.id) AS total_books,
    COUNT(l.id) AS total_loans,
    ROUND(COUNT(l.id) * 1.0 / COUNT(DISTINCT b.id), 2) AS avg_loans_per_book
FROM books b
LEFT JOIN loans l ON b.id = l.book_id
GROUP BY b.genre
ORDER BY total_loans DESC;

-- ------------------------------------------------------------
-- 6. Members who have never borrowed a book
-- ------------------------------------------------------------
SELECT
    m.id,
    m.name,
    m.email,
    m.joined_date
FROM members m
LEFT JOIN loans l ON m.id = l.member_id
WHERE l.id IS NULL
  AND m.is_active = 1;

-- ------------------------------------------------------------
-- 7. Monthly loan trends (current year)
-- ------------------------------------------------------------
SELECT
    strftime('%Y-%m', loan_date) AS month,
    COUNT(*) AS total_loans,
    SUM(CASE WHEN return_date IS NOT NULL THEN 1 ELSE 0 END) AS returned,
    SUM(CASE WHEN return_date IS NULL AND due_date < DATE('now') THEN 1 ELSE 0 END) AS overdue
FROM loans
WHERE loan_date >= DATE('now', 'start of year')
GROUP BY strftime('%Y-%m', loan_date)
ORDER BY month;

-- ------------------------------------------------------------
-- 8. Most active members (by loan count)
-- ------------------------------------------------------------
SELECT
    m.name,
    m.email,
    COUNT(l.id) AS total_loans,
    ROUND(AVG(julianday(l.return_date) - julianday(l.loan_date)), 2) AS avg_loan_duration_days,
    SUM(f.amount) AS total_fines
FROM members m
JOIN loans l ON m.id = l.member_id
LEFT JOIN fines f ON l.id = f.loan_id
WHERE l.return_date IS NOT NULL
GROUP BY m.id, m.name, m.email
ORDER BY total_loans DESC
LIMIT 10;

-- ------------------------------------------------------------
-- 9. Books that have never been borrowed
-- ------------------------------------------------------------
SELECT
    b.title,
    b.author,
    b.genre,
    b.copies_total
FROM books b
LEFT JOIN loans l ON b.id = l.book_id
WHERE l.id IS NULL;

-- ------------------------------------------------------------
-- 10. Revenue from fines (paid vs unpaid)
-- ------------------------------------------------------------
SELECT
    SUM(CASE WHEN paid = 1 THEN amount ELSE 0 END) AS total_paid,
    SUM(CASE WHEN paid = 0 THEN amount ELSE 0 END) AS total_unpaid,
    SUM(amount) AS total_fines
FROM fines;

-- ------------------------------------------------------------
-- 11. Members with active loans and their email (for notifications)
-- ------------------------------------------------------------
SELECT
    m.name,
    m.email,
    COUNT(l.id) AS active_loans,
    GROUP_CONCAT(b.title, ', ') AS borrowed_books
FROM members m
JOIN loans l ON m.id = l.member_id
JOIN books b ON l.book_id = b.id
WHERE l.return_date IS NULL
GROUP BY m.id, m.name, m.email
HAVING active_loans > 0;

-- ------------------------------------------------------------
-- 12. Overdue loan details with calculated fines
-- ------------------------------------------------------------
SELECT
    m.name AS member_name,
    m.email,
    b.title AS book_title,
    l.loan_date,
    l.due_date,
    (julianday('now') - julianday(l.due_date)) AS days_overdue,
    ROUND((julianday('now') - julianday(l.due_date)) * 0.50, 2) AS fine_amount
FROM loans l
JOIN members m ON l.member_id = m.id
JOIN books b ON l.book_id = b.id
WHERE l.return_date IS NULL
  AND l.due_date < DATE('now')
ORDER BY days_overdue DESC;

-- ------------------------------------------------------------
-- 13. Add a new loan (with automatic availability check)
-- ------------------------------------------------------------
-- Note: The trigger trg_prevent_loan_when_no_copies will prevent
-- loan creation if no copies are available.

-- Example:
-- INSERT INTO loans (book_id, member_id, due_date)
-- VALUES (1, 1, DATE('now', '+14 days'));

-- ------------------------------------------------------------
-- 14. Return a book (automatic updates via triggers)
-- ------------------------------------------------------------
-- Example:
-- UPDATE loans
-- SET return_date = DATE('now'),
--     status = 'returned'
-- WHERE id = 1;

-- ------------------------------------------------------------
-- 15. Pay a fine
-- ------------------------------------------------------------
-- Example:
-- UPDATE fines
-- SET paid = 1,
--     paid_date = DATE('now')
-- WHERE id = 1;
