-- ============================================================
-- Sales Analytics – Analytical Queries
-- ============================================================

-- ------------------------------------------------------------
-- 1. Total revenue by month (2024)
-- ------------------------------------------------------------
SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(s.revenue) AS total_revenue
FROM sales s
JOIN dim_date d ON s.date_id = d.date_id
WHERE d.year = 2024
GROUP BY d.year, d.month, d.month_name
ORDER BY d.month;

-- ------------------------------------------------------------
-- 2. Top 5 products by revenue (all time)
-- ------------------------------------------------------------
SELECT
    p.product_name,
    p.category,
    SUM(s.revenue) AS total_revenue,
    COUNT(s.sale_id) AS sales_count
FROM sales s
JOIN dim_product p ON s.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 5;

-- ------------------------------------------------------------
-- 3. Monthly revenue trend with moving average (3-month rolling)
-- ------------------------------------------------------------
WITH monthly_revenue AS (
    SELECT
        d.year,
        d.month,
        d.month_name,
        SUM(s.revenue) AS revenue
    FROM sales s
    JOIN dim_date d ON s.date_id = d.date_id
    GROUP BY d.year, d.month, d.month_name
)
SELECT
    year,
    month,
    month_name,
    revenue,
    AVG(revenue) OVER (ORDER BY year, month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS three_month_avg
FROM monthly_revenue
ORDER BY year, month;

-- ------------------------------------------------------------
-- 4. Sales by region and category
-- ------------------------------------------------------------
SELECT
    st.region,
    p.category,
    SUM(s.revenue) AS total_revenue,
    COUNT(s.sale_id) AS total_sales
FROM sales s
JOIN dim_store st ON s.store_id = st.store_id
JOIN dim_product p ON s.product_id = p.product_id
GROUP BY st.region, p.category
ORDER BY st.region, total_revenue DESC;

-- ------------------------------------------------------------
-- 5. Top 10 customers by revenue
-- ------------------------------------------------------------
SELECT
    c.first_name || ' ' || c.last_name AS customer_name,
    c.membership_level,
    SUM(s.revenue) AS total_spent,
    COUNT(s.sale_id) AS order_count
FROM sales s
JOIN dim_customer c ON s.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.membership_level
ORDER BY total_spent DESC
LIMIT 10;

-- ------------------------------------------------------------
-- 6. Monthly revenue vs. previous month (percentage change)
-- ------------------------------------------------------------
WITH monthly_revenue AS (
    SELECT
        d.year,
        d.month,
        SUM(s.revenue) AS revenue
    FROM sales s
    JOIN dim_date d ON s.date_id = d.date_id
    GROUP BY d.year, d.month
)
SELECT
    year,
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY year, month) AS previous_month_revenue,
    CASE
        WHEN LAG(revenue) OVER (ORDER BY year, month) IS NULL THEN NULL
        ELSE ROUND((revenue - LAG(revenue) OVER (ORDER BY year, month)) * 100.0 / LAG(revenue) OVER (ORDER BY year, month), 2)
    END AS pct_change
FROM monthly_revenue
ORDER BY year, month;

-- ------------------------------------------------------------
-- 7. Top 5 selling products in each region (rank)
-- ------------------------------------------------------------
WITH ranked_products AS (
    SELECT
        st.region,
        p.product_name,
        SUM(s.revenue) AS total_revenue,
        RANK() OVER (PARTITION BY st.region ORDER BY SUM(s.revenue) DESC) AS rank_num
    FROM sales s
    JOIN dim_store st ON s.store_id = st.store_id
    JOIN dim_product p ON s.product_id = p.product_id
    GROUP BY st.region, p.product_id, p.product_name
)
SELECT
    region,
    product_name,
    total_revenue,
    rank_num
FROM ranked_products
WHERE rank_num <= 5
ORDER BY region, rank_num;

-- ------------------------------------------------------------
-- 8. Sales performance by quarter (year-over-year)
-- ------------------------------------------------------------
SELECT
    d.year,
    d.quarter,
    SUM(s.revenue) AS total_revenue,
    LAG(SUM(s.revenue)) OVER (PARTITION BY d.quarter ORDER BY d.year) AS previous_year_revenue,
    CASE
        WHEN LAG(SUM(s.revenue)) OVER (PARTITION BY d.quarter ORDER BY d.year) IS NULL THEN NULL
        ELSE ROUND((SUM(s.revenue) - LAG(SUM(s.revenue)) OVER (PARTITION BY d.quarter ORDER BY d.year)) * 100.0 / LAG(SUM(s.revenue)) OVER (PARTITION BY d.quarter ORDER BY d.year), 2)
    END AS yoy_pct_change
FROM sales s
JOIN dim_date d ON s.date_id = d.date_id
GROUP BY d.year, d.quarter
ORDER BY d.year, d.quarter;

-- ------------------------------------------------------------
-- 9. Weekend vs. weekday sales
-- ------------------------------------------------------------
SELECT
    CASE WHEN d.is_weekend = 1 THEN 'Weekend' ELSE 'Weekday' END AS day_type,
    SUM(s.revenue) AS total_revenue,
    COUNT(s.sale_id) AS total_transactions,
    AVG(s.revenue) AS avg_transaction_value
FROM sales s
JOIN dim_date d ON s.date_id = d.date_id
GROUP BY d.is_weekend;

-- ------------------------------------------------------------
-- 10. Customer lifetime value by membership level
-- ------------------------------------------------------------
SELECT
    c.membership_level,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    SUM(s.revenue) AS total_revenue,
    AVG(s.revenue) AS avg_transaction_value,
    SUM(s.revenue) / COUNT(DISTINCT c.customer_id) AS avg_lifetime_value
FROM sales s
JOIN dim_customer c ON s.customer_id = c.customer_id
GROUP BY c.membership_level
ORDER BY avg_lifetime_value DESC;

-- ------------------------------------------------------------
-- 11. Daily sales with cumulative sum (running total)
-- ------------------------------------------------------------
SELECT
    d.full_date,
    SUM(s.revenue) AS daily_revenue,
    SUM(SUM(s.revenue)) OVER (ORDER BY d.full_date) AS cumulative_revenue
FROM sales s
JOIN dim_date d ON s.date_id = d.date_id
GROUP BY d.full_date
ORDER BY d.full_date;

-- ------------------------------------------------------------
-- 12. Store performance by month (ranking within region)
-- ------------------------------------------------------------
WITH store_monthly AS (
    SELECT
        st.region,
        st.store_name,
        d.year,
        d.month,
        SUM(s.revenue) AS total_revenue,
        RANK() OVER (PARTITION BY st.region, d.year, d.month ORDER BY SUM(s.revenue) DESC) AS rank_in_region
    FROM sales s
    JOIN dim_store st ON s.store_id = st.store_id
    JOIN dim_date d ON s.date_id = d.date_id
    GROUP BY st.region, st.store_id, d.year, d.month
)
SELECT
    region,
    store_name,
    year,
    month,
    total_revenue,
    rank_in_region
FROM store_monthly
WHERE rank_in_region <= 3
ORDER BY region, year, month, rank_in_region;

-- ------------------------------------------------------------
-- 13. Most popular product by customer age group
-- ------------------------------------------------------------
SELECT
    CASE
        WHEN c.age < 25 THEN '18-24'
        WHEN c.age BETWEEN 25 AND 34 THEN '25-34'
        WHEN c.age BETWEEN 35 AND 44 THEN '35-44'
        WHEN c.age BETWEEN 45 AND 54 THEN '45-54'
        ELSE '55+'
    END AS age_group,
    p.product_name,
    COUNT(s.sale_id) AS purchase_count
FROM sales s
JOIN dim_customer c ON s.customer_id = c.customer_id
JOIN dim_product p ON s.product_id = p.product_id
GROUP BY age_group, p.product_id, p.product_name
ORDER BY age_group, purchase_count DESC;

-- ------------------------------------------------------------
-- 14. Sales with discount vs. without discount
-- ------------------------------------------------------------
SELECT
    CASE WHEN s.discount > 0 THEN 'With Discount' ELSE 'Without Discount' END AS discount_status,
    COUNT(s.sale_id) AS transaction_count,
    SUM(s.revenue) AS total_revenue,
    AVG(s.revenue) AS avg_revenue
FROM sales s
GROUP BY discount_status;

-- ------------------------------------------------------------
-- 15. Contribution to total revenue by category (percentage)
-- ------------------------------------------------------------
SELECT
    p.category,
    SUM(s.revenue) AS category_revenue,
    ROUND(SUM(s.revenue) * 100.0 / (SELECT SUM(revenue) FROM sales), 2) AS percentage_of_total
FROM sales s
JOIN dim_product p ON s.product_id = p.product_id
GROUP BY p.category
ORDER BY percentage_of_total DESC;
