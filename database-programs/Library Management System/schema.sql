-- ============================================================
-- Library Management System – Database Schema (Simplified)
-- SQLite 3.x compatible
-- ============================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- Table: books
-- ------------------------------------------------------------
CREATE TABLE books (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    title           TEXT NOT NULL,
    author          TEXT NOT NULL,
    isbn            TEXT UNIQUE NOT NULL,
    genre           TEXT NOT NULL,
    published_year  INTEGER NOT NULL,
    copies_total    INTEGER NOT NULL DEFAULT 1 CHECK (copies_total >= 1),
    copies_available INTEGER NOT NULL DEFAULT 1 CHECK (copies_available >= 0),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Table: members
-- ------------------------------------------------------------
CREATE TABLE members (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    email           TEXT UNIQUE NOT NULL,
    phone           TEXT,
    address         TEXT,
    membership_type TEXT NOT NULL DEFAULT 'standard' CHECK (membership_type IN ('standard', 'premium', 'student')),
    joined_date     DATE NOT NULL DEFAULT CURRENT_DATE,
    is_active       BOOLEAN NOT NULL DEFAULT 1,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Table: loans
-- ------------------------------------------------------------
CREATE TABLE loans (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id         INTEGER NOT NULL REFERENCES books(id) ON DELETE RESTRICT,
    member_id       INTEGER NOT NULL REFERENCES members(id) ON DELETE RESTRICT,
    loan_date       DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date        DATE NOT NULL,
    return_date     DATE,
    status          TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'returned', 'overdue')),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Table: fines
-- ------------------------------------------------------------
CREATE TABLE fines (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id         INTEGER NOT NULL REFERENCES loans(id) ON DELETE CASCADE,
    amount          DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    paid            BOOLEAN NOT NULL DEFAULT 0,
    paid_date       DATE,
    description     TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Table: categories
-- ------------------------------------------------------------
CREATE TABLE categories (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT UNIQUE NOT NULL,
    description     TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Indexes (for performance)
-- ------------------------------------------------------------
CREATE INDEX idx_books_isbn ON books(isbn);
CREATE INDEX idx_books_title ON books(title);
CREATE INDEX idx_books_author ON books(author);
CREATE INDEX idx_books_genre ON books(genre);

CREATE INDEX idx_members_email ON members(email);
CREATE INDEX idx_members_name ON members(name);

CREATE INDEX idx_loans_book_id ON loans(book_id);
CREATE INDEX idx_loans_member_id ON loans(member_id);
CREATE INDEX idx_loans_status ON loans(status);
CREATE INDEX idx_loans_due_date ON loans(due_date);
CREATE INDEX idx_loans_loan_date ON loans(loan_date);

CREATE INDEX idx_fines_loan_id ON fines(loan_id);
CREATE INDEX idx_fines_paid ON fines(paid);
