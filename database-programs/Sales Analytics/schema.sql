-- ============================================================
-- Sales Analytics – Star Schema
-- SQLite 3.x compatible
-- ============================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- Dimension: dim_date
-- ------------------------------------------------------------
CREATE TABLE dim_date (
    date_id         INTEGER PRIMARY KEY,   -- YYYYMMDD format
    full_date       DATE UNIQUE NOT NULL,
    year            INTEGER NOT NULL,
    quarter         INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    month           INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    month_name      TEXT NOT NULL,
    day             INTEGER NOT NULL CHECK (day BETWEEN 1 AND 31),
    day_of_week     INTEGER NOT NULL CHECK (day_of_week BETWEEN 1 AND 7),
    day_name        TEXT NOT NULL,
    is_weekend      BOOLEAN NOT NULL DEFAULT 0,
    is_holiday      BOOLEAN NOT NULL DEFAULT 0
);

-- ------------------------------------------------------------
-- Dimension: dim_product
-- ------------------------------------------------------------
CREATE TABLE dim_product (
    product_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name    TEXT NOT NULL,
    category        TEXT NOT NULL,
    subcategory     TEXT NOT NULL,
    brand           TEXT,
    unit_price      DECIMAL(10,2) NOT NULL CHECK (unit_price > 0)
);

-- ------------------------------------------------------------
-- Dimension: dim_store
-- ------------------------------------------------------------
CREATE TABLE dim_store (
    store_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    store_name      TEXT NOT NULL,
    location        TEXT NOT NULL,
    city            TEXT NOT NULL,
    state           TEXT NOT NULL,
    region          TEXT NOT NULL
);

-- ------------------------------------------------------------
-- Dimension: dim_customer
-- ------------------------------------------------------------
CREATE TABLE dim_customer (
    customer_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    email           TEXT UNIQUE,
    phone           TEXT,
    city            TEXT,
    state           TEXT,
    age             INTEGER,
    gender          TEXT CHECK (gender IN ('M', 'F', 'Other')),
    membership_level TEXT DEFAULT 'Standard' CHECK (membership_level IN ('Standard', 'Gold', 'Platinum'))
);

-- ------------------------------------------------------------
-- Fact: sales
-- ------------------------------------------------------------
CREATE TABLE sales (
    sale_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    date_id         INTEGER NOT NULL REFERENCES dim_date(date_id),
    product_id      INTEGER NOT NULL REFERENCES dim_product(product_id),
    store_id        INTEGER NOT NULL REFERENCES dim_store(store_id),
    customer_id     INTEGER NOT NULL REFERENCES dim_customer(customer_id),
    quantity        INTEGER NOT NULL CHECK (quantity > 0),
    unit_price      DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    discount        DECIMAL(10,2) NOT NULL DEFAULT 0.00 CHECK (discount >= 0),
    revenue         DECIMAL(10,2) NOT NULL CHECK (revenue >= 0),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Indexes for performance
-- ------------------------------------------------------------
CREATE INDEX idx_sales_date_id ON sales(date_id);
CREATE INDEX idx_sales_product_id ON sales(product_id);
CREATE INDEX idx_sales_store_id ON sales(store_id);
CREATE INDEX idx_sales_customer_id ON sales(customer_id);
CREATE INDEX idx_sales_revenue ON sales(revenue);

CREATE INDEX idx_dim_date_full_date ON dim_date(full_date);
CREATE INDEX idx_dim_product_category ON dim_product(category);
CREATE INDEX idx_dim_store_region ON dim_store(region);
CREATE INDEX idx_dim_customer_state ON dim_customer(state);

-- ------------------------------------------------------------
-- View: sales with all dimensions (denormalized for reporting)
-- ------------------------------------------------------------
CREATE VIEW v_sales_full AS
SELECT
    s.sale_id,
    d.full_date,
    d.year,
    d.quarter,
    d.month,
    d.month_name,
    d.day_of_week,
    d.day_name,
    d.is_weekend,
    p.product_name,
    p.category,
    p.subcategory,
    p.brand,
    st.store_name,
    st.location,
    st.city AS store_city,
    st.state AS store_state,
    st.region,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email AS customer_email,
    c.city AS customer_city,
    c.state AS customer_state,
    c.age AS customer_age,
    c.gender AS customer_gender,
    c.membership_level,
    s.quantity,
    s.unit_price,
    s.discount,
    s.revenue
FROM sales s
JOIN dim_date d ON s.date_id = d.date_id
JOIN dim_product p ON s.product_id = p.product_id
JOIN dim_store st ON s.store_id = st.store_id
JOIN dim_customer c ON s.customer_id = c.customer_id;
