-- ============================================================
-- Sales Analytics – Sample Data (Clean, Working)
-- ============================================================

-- ------------------------------------------------------------
-- Populate dim_date (generate 3 years of dates – 2023, 2024, 2025)
-- ------------------------------------------------------------
WITH RECURSIVE date_range AS (
    SELECT '2023-01-01' AS dt
    UNION ALL
    SELECT DATE(dt, '+1 day')
    FROM date_range
    WHERE dt < '2025-12-31'
)
INSERT INTO dim_date (date_id, full_date, year, quarter, month, month_name, day, day_of_week, day_name, is_weekend)
SELECT
    CAST(strftime('%Y%m%d', dt) AS INTEGER) AS date_id,
    dt AS full_date,
    CAST(strftime('%Y', dt) AS INTEGER) AS year,
    CASE
        WHEN CAST(strftime('%m', dt) AS INTEGER) BETWEEN 1 AND 3 THEN 1
        WHEN CAST(strftime('%m', dt) AS INTEGER) BETWEEN 4 AND 6 THEN 2
        WHEN CAST(strftime('%m', dt) AS INTEGER) BETWEEN 7 AND 9 THEN 3
        ELSE 4
    END AS quarter,
    CAST(strftime('%m', dt) AS INTEGER) AS month,
    CASE CAST(strftime('%m', dt) AS INTEGER)
        WHEN 1 THEN 'January' WHEN 2 THEN 'February' WHEN 3 THEN 'March'
        WHEN 4 THEN 'April' WHEN 5 THEN 'May' WHEN 6 THEN 'June'
        WHEN 7 THEN 'July' WHEN 8 THEN 'August' WHEN 9 THEN 'September'
        WHEN 10 THEN 'October' WHEN 11 THEN 'November' WHEN 12 THEN 'December'
    END AS month_name,
    CAST(strftime('%d', dt) AS INTEGER) AS day,
    CAST(strftime('%w', dt) AS INTEGER) + 1 AS day_of_week,
    CASE CAST(strftime('%w', dt) AS INTEGER)
        WHEN 0 THEN 'Sunday' WHEN 1 THEN 'Monday' WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday' WHEN 4 THEN 'Thursday' WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS day_name,
    CASE WHEN CAST(strftime('%w', dt) AS INTEGER) IN (0, 6) THEN 1 ELSE 0 END AS is_weekend
FROM date_range;

-- ------------------------------------------------------------
-- Populate dim_product
-- ------------------------------------------------------------
INSERT INTO dim_product (product_name, category, subcategory, brand, unit_price) VALUES
    ('Laptop Pro 15', 'Electronics', 'Laptops', 'TechBrand', 1200.00),
    ('Ultrabook 13', 'Electronics', 'Laptops', 'TechBrand', 950.00),
    ('Gaming Laptop X', 'Electronics', 'Laptops', 'GameMaster', 1500.00),
    ('Wireless Mouse', 'Electronics', 'Accessories', 'AccessoryWorld', 25.00),
    ('Mechanical Keyboard', 'Electronics', 'Accessories', 'AccessoryWorld', 80.00),
    ('USB-C Hub', 'Electronics', 'Accessories', 'AccessoryWorld', 45.00),
    ('Bluetooth Headphones', 'Electronics', 'Audio', 'SoundPro', 150.00),
    ('Noise Cancelling Headphones', 'Electronics', 'Audio', 'SoundPro', 250.00),
    ('Smartphone 5G', 'Electronics', 'Phones', 'PhoneCo', 800.00),
    ('Smartphone Pro', 'Electronics', 'Phones', 'PhoneCo', 1100.00),
    ('Tablet 10', 'Electronics', 'Tablets', 'TechBrand', 400.00),
    ('Tablet Pro', 'Electronics', 'Tablets', 'TechBrand', 650.00),
    ('Office Chair', 'Furniture', 'Chairs', 'Comfort Inc', 200.00),
    ('Desk Lamp', 'Furniture', 'Lighting', 'LightWorks', 35.00),
    ('Bookshelf', 'Furniture', 'Shelving', 'HomeStyle', 120.00),
    ('Coffee Table', 'Furniture', 'Tables', 'HomeStyle', 180.00),
    ('Running Shoes', 'Apparel', 'Footwear', 'SportsGear', 120.00),
    ('Yoga Mat', 'Apparel', 'Sports Equipment', 'SportsGear', 30.00),
    ('T-Shirt', 'Apparel', 'Clothing', 'FashionCo', 20.00),
    ('Jeans', 'Apparel', 'Clothing', 'FashionCo', 60.00);

-- ------------------------------------------------------------
-- Populate dim_store
-- ------------------------------------------------------------
INSERT INTO dim_store (store_name, location, city, state, region) VALUES
    ('Downtown Mall', '123 Main St', 'New York', 'NY', 'East'),
    ('Uptown Plaza', '456 High St', 'Los Angeles', 'CA', 'West'),
    ('Midtown Center', '789 Park Ave', 'Chicago', 'IL', 'Central'),
    ('Eastside Corner', '321 Oak St', 'Houston', 'TX', 'South'),
    ('Northgate', '654 Pine St', 'Phoenix', 'AZ', 'West'),
    ('Southfield', '987 Cedar Ln', 'Philadelphia', 'PA', 'East'),
    ('Westlake', '147 Maple Dr', 'San Antonio', 'TX', 'South'),
    ('Bayview', '258 Spruce Ave', 'San Diego', 'CA', 'West');

-- ------------------------------------------------------------
-- Populate dim_customer
-- ------------------------------------------------------------
INSERT INTO dim_customer (first_name, last_name, email, phone, city, state, age, gender, membership_level) VALUES
    ('John', 'Smith', 'john.s@email.com', '555-0101', 'New York', 'NY', 35, 'M', 'Gold'),
    ('Emily', 'Johnson', 'emily.j@email.com', '555-0102', 'Los Angeles', 'CA', 28, 'F', 'Standard'),
    ('Michael', 'Brown', 'michael.b@email.com', '555-0103', 'Chicago', 'IL', 42, 'M', 'Platinum'),
    ('Sarah', 'Wilson', 'sarah.w@email.com', '555-0104', 'Houston', 'TX', 31, 'F', 'Standard'),
    ('David', 'Martinez', 'david.m@email.com', '555-0105', 'Phoenix', 'AZ', 55, 'M', 'Gold'),
    ('Lisa', 'Anderson', 'lisa.a@email.com', '555-0106', 'Philadelphia', 'PA', 29, 'F', 'Standard'),
    ('James', 'Taylor', 'james.t@email.com', '555-0107', 'San Antonio', 'TX', 47, 'M', 'Platinum'),
    ('Maria', 'Garcia', 'maria.g@email.com', '555-0108', 'San Diego', 'CA', 33, 'F', 'Gold'),
    ('Robert', 'Kim', 'robert.k@email.com', '555-0109', 'New York', 'NY', 26, 'M', 'Standard'),
    ('Jennifer', 'Lee', 'jennifer.l@email.com', '555-0110', 'Los Angeles', 'CA', 39, 'F', 'Platinum');

-- ------------------------------------------------------------
-- Populate sales – Manual fixed data (2024 and 2025)
-- ------------------------------------------------------------

-- 2024 sales
INSERT INTO sales (date_id, product_id, store_id, customer_id, quantity, unit_price, discount, revenue) VALUES
    (20240115, 1, 1, 1, 2, 1200, 0.05, 2280),
    (20240120, 3, 2, 2, 1, 1500, 0.00, 1500),
    (20240210, 5, 3, 3, 4, 80, 0.00, 320),
    (20240214, 9, 4, 4, 3, 800, 0.10, 2160),
    (20240301, 2, 5, 5, 1, 950, 0.00, 950),
    (20240315, 11, 6, 6, 2, 400, 0.00, 800),
    (20240405, 17, 7, 7, 3, 120, 0.05, 342),
    (20240420, 19, 8, 8, 5, 20, 0.00, 100),
    (20240501, 4, 1, 9, 10, 25, 0.00, 250),
    (20240515, 7, 2, 10, 2, 150, 0.00, 300),
    (20240601, 10, 3, 1, 1, 1100, 0.00, 1100),
    (20240615, 13, 4, 2, 2, 200, 0.10, 360),
    (20240704, 14, 5, 3, 1, 35, 0.00, 35),
    (20240720, 16, 6, 4, 3, 180, 0.00, 540),
    (20240801, 18, 7, 5, 4, 30, 0.00, 120),
    (20240815, 20, 8, 6, 2, 60, 0.00, 120),
    (20240901, 6, 1, 7, 5, 45, 0.05, 213.75),
    (20240915, 8, 2, 8, 1, 250, 0.00, 250),
    (20241001, 12, 3, 9, 3, 650, 0.00, 1950),
    (20241015, 15, 4, 10, 2, 120, 0.00, 240),
    (20241101, 1, 5, 1, 1, 1200, 0.00, 1200),
    (20241115, 3, 6, 2, 2, 1500, 0.10, 2700),
    (20241201, 5, 7, 3, 1, 80, 0.00, 80),
    (20241225, 9, 8, 4, 3, 800, 0.10, 2160),
    (20240310, 5, 1, 9, 2, 80, 0.00, 160),
    (20240610, 10, 2, 10, 1, 1100, 0.00, 1100),
    (20240910, 12, 3, 1, 2, 650, 0.05, 1235),
    (20241210, 14, 4, 2, 1, 35, 0.00, 35);

-- 2025 sales
INSERT INTO sales (date_id, product_id, store_id, customer_id, quantity, unit_price, discount, revenue) VALUES
    (20250105, 11, 1, 5, 2, 400, 0.00, 800),
    (20250115, 13, 2, 6, 1, 200, 0.00, 200),
    (20250201, 17, 3, 7, 3, 120, 0.05, 342),
    (20250214, 19, 4, 8, 4, 20, 0.00, 80),
    (20250301, 2, 5, 9, 1, 950, 0.00, 950),
    (20250315, 4, 6, 10, 10, 25, 0.00, 250),
    (20250401, 7, 7, 1, 2, 150, 0.00, 300),
    (20250415, 10, 8, 2, 1, 1100, 0.00, 1100),
    (20250501, 14, 1, 3, 2, 35, 0.00, 70),
    (20250515, 16, 2, 4, 3, 180, 0.00, 540),
    (20250601, 18, 3, 5, 4, 30, 0.00, 120),
    (20250615, 20, 4, 6, 2, 60, 0.00, 120),
    (20250704, 6, 5, 7, 5, 45, 0.05, 213.75),
    (20250720, 8, 6, 8, 1, 250, 0.00, 250),
    (20250801, 12, 7, 9, 3, 650, 0.00, 1950),
    (20250815, 15, 8, 10, 2, 120, 0.00, 240),
    (20250901, 1, 1, 1, 1, 1200, 0.00, 1200),
    (20250915, 3, 2, 2, 2, 1500, 0.10, 2700),
    (20251001, 5, 3, 3, 1, 80, 0.00, 80),
    (20251015, 9, 4, 4, 3, 800, 0.10, 2160),
    (20251101, 11, 5, 5, 2, 400, 0.00, 800),
    (20251115, 13, 6, 6, 1, 200, 0.00, 200),
    (20251201, 17, 7, 7, 3, 120, 0.05, 342),
    (20251225, 19, 8, 8, 4, 20, 0.00, 80),
    (20250220, 16, 5, 3, 3, 180, 0.00, 540),
    (20250520, 18, 6, 4, 2, 30, 0.00, 60),
    (20250820, 20, 7, 5, 4, 60, 0.00, 240),
    (20251120, 6, 8, 6, 2, 45, 0.00, 90);
