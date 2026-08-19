-- ============================================================
-- Library Management System – Sample Data
-- ============================================================

-- Categories
INSERT INTO categories (name, description) VALUES
    ('Fiction', 'Fictional books'),
    ('Non-Fiction', 'Non-fictional books'),
    ('Science', 'Scientific books'),
    ('Technology', 'Technology and programming books'),
    ('History', 'Historical books'),
    ('Biography', 'Biographical books'),
    ('Fantasy', 'Fantasy fiction'),
    ('Romance', 'Romance fiction'),
    ('Thriller', 'Thriller and suspense fiction'),
    ('Science Fiction', 'Sci-fi books');

-- Books
INSERT INTO books (title, author, isbn, genre, published_year, copies_total, copies_available) VALUES
    ('To Kill a Mockingbird', 'Harper Lee', '978-0061120084', 'Fiction', 1960, 5, 5),
    ('1984', 'George Orwell', '978-0451524935', 'Fiction', 1949, 3, 3),
    ('The Great Gatsby', 'F. Scott Fitzgerald', '978-0743273565', 'Fiction', 1925, 4, 4),
    ('The Catcher in the Rye', 'J.D. Salinger', '978-0316769488', 'Fiction', 1951, 2, 2),
    ('Brave New World', 'Aldous Huxley', '978-0060850524', 'Science Fiction', 1932, 3, 3),
    ('The Hobbit', 'J.R.R. Tolkien', '978-0547928227', 'Fantasy', 1937, 5, 5),
    ('The Lord of the Rings', 'J.R.R. Tolkien', '978-0544003415', 'Fantasy', 1954, 3, 3),
    ('Pride and Prejudice', 'Jane Austen', '978-0141439518', 'Romance', 1813, 4, 4),
    ('The Alchemist', 'Paulo Coelho', '978-0061122415', 'Fiction', 1988, 2, 2),
    ('The Da Vinci Code', 'Dan Brown', '978-0385504201', 'Thriller', 2003, 3, 3),
    ('Sapiens', 'Yuval Noah Harari', '978-0062316097', 'History', 2011, 4, 4),
    ('A Brief History of Time', 'Stephen Hawking', '978-0553380163', 'Science', 1988, 2, 2),
    ('The Art of War', 'Sun Tzu', '978-1590302259', 'History', -500, 3, 3),
    ('Clean Code', 'Robert C. Martin', '978-0132350884', 'Technology', 2008, 3, 3),
    ('The Pragmatic Programmer', 'Andrew Hunt', '978-0201616224', 'Technology', 1999, 2, 2),
    ('Design Patterns', 'Erich Gamma', '978-0201633610', 'Technology', 1994, 2, 2),
    ('Thinking, Fast and Slow', 'Daniel Kahneman', '978-0374533557', 'Non-Fiction', 2011, 3, 3),
    ('The Selfish Gene', 'Richard Dawkins', '978-0199291151', 'Science', 1976, 2, 2),
    ('The Odyssey', 'Homer', '978-0140268867', 'Fiction', -800, 2, 2),
    ('War and Peace', 'Leo Tolstoy', '978-1400079988', 'Fiction', 1869, 2, 2);

-- Members
INSERT INTO members (name, email, phone, address, membership_type, joined_date, is_active) VALUES
    ('John Smith', 'john.smith@email.com', '555-0101', '123 Main St, New York, NY 10001', 'premium', '2024-01-15', 1),
    ('Emily Johnson', 'emily.j@email.com', '555-0102', '456 Oak Ave, Los Angeles, CA 90001', 'standard', '2024-02-20', 1),
    ('Michael Brown', 'michael.brown@email.com', '555-0103', '789 Pine Rd, Chicago, IL 60601', 'student', '2024-03-10', 1),
    ('Sarah Wilson', 'sarah.w@email.com', '555-0104', '321 Elm St, Houston, TX 77001', 'standard', '2024-04-05', 1),
    ('David Martinez', 'david.m@email.com', '555-0105', '654 Cedar Ln, Phoenix, AZ 85001', 'premium', '2024-05-12', 1),
    ('Lisa Anderson', 'lisa.a@email.com', '555-0106', '987 Birch Dr, Philadelphia, PA 19101', 'standard', '2024-06-18', 1),
    ('James Taylor', 'james.t@email.com', '555-0107', '147 Maple St, San Antonio, TX 78201', 'student', '2024-07-22', 1),
    ('Maria Garcia', 'maria.g@email.com', '555-0108', '258 Walnut Ave, San Diego, CA 92101', 'standard', '2024-08-30', 1),
    ('Robert Kim', 'robert.k@email.com', '555-0109', '369 Spruce Rd, Dallas, TX 75201', 'premium', '2024-09-14', 1),
    ('Jennifer Lee', 'jennifer.l@email.com', '555-0110', '741 Ash St, San Jose, CA 95101', 'standard', '2024-10-01', 1),
    ('William Wong', 'william.w@email.com', '555-0111', '852 Fir Dr, Austin, TX 78701', 'student', '2024-10-15', 1),
    ('Patricia Chen', 'patricia.c@email.com', '555-0112', '963 Oak Ln, Jacksonville, FL 32201', 'standard', '2024-11-01', 1),
    ('Thomas White', 'thomas.w@email.com', '555-0113', '159 Pine St, Fort Worth, TX 76101', 'premium', '2024-11-20', 1),
    ('Elizabeth Taylor', 'elizabeth.t@email.com', '555-0114', '258 Cedar Ave, Columbus, OH 43201', 'standard', '2024-12-01', 1);

-- Loans (mix of active, returned, and overdue)
INSERT INTO loans (book_id, member_id, loan_date, due_date, return_date, status) VALUES
    -- Returned loans
    (1, 1, '2024-01-20', '2024-02-03', '2024-02-01', 'returned'),
    (2, 2, '2024-02-25', '2024-03-10', '2024-03-05', 'returned'),
    (3, 3, '2024-03-15', '2024-03-29', '2024-03-28', 'returned'),
    (4, 4, '2024-04-10', '2024-04-24', '2024-04-20', 'returned'),
    (5, 5, '2024-05-15', '2024-05-29', '2024-05-25', 'returned'),
    (6, 6, '2024-06-20', '2024-07-04', '2024-07-01', 'returned'),
    (7, 7, '2024-07-25', '2024-08-08', '2024-08-05', 'returned'),
    (8, 8, '2024-08-30', '2024-09-13', '2024-09-10', 'returned'),
    (9, 9, '2024-09-15', '2024-09-29', '2024-09-28', 'returned'),
    (10, 10, '2024-10-01', '2024-10-15', '2024-10-12', 'returned'),
    -- Active loans
    (11, 1, '2024-11-01', '2024-11-15', NULL, 'active'),
    (12, 2, '2024-11-05', '2024-11-19', NULL, 'active'),
    (13, 3, '2024-11-10', '2024-11-24', NULL, 'active'),
    (14, 4, '2024-11-12', '2024-11-26', NULL, 'active'),
    (15, 5, '2024-11-15', '2024-11-29', NULL, 'active'),
    -- Overdue loans
    (16, 6, '2024-10-20', '2024-11-03', NULL, 'overdue'),
    (17, 7, '2024-10-25', '2024-11-08', NULL, 'overdue'),
    (18, 8, '2024-10-30', '2024-11-13', NULL, 'overdue'),
    (19, 9, '2024-11-01', '2024-11-15', NULL, 'overdue'),
    (20, 10, '2024-11-02', '2024-11-16', NULL, 'overdue');

-- Fines
INSERT INTO fines (loan_id, amount, paid, paid_date, description) VALUES
    (1, 0.50, 1, '2024-02-02', 'Late return: due 2024-02-03, returned 2024-02-04'),
    (2, 1.00, 1, '2024-03-06', 'Late return: due 2024-03-10, returned 2024-03-12'),
    (16, 1.50, 0, NULL, 'Overdue 3 days'),
    (17, 2.00, 0, NULL, 'Overdue 4 days'),
    (18, 2.50, 0, NULL, 'Overdue 5 days');
