-- ============================================================
-- Log Analysis – Analytical Queries
-- ============================================================

-- ------------------------------------------------------------
-- 1. Total requests, errors, average response time per day
-- ------------------------------------------------------------
SELECT
    DATE(log_timestamp) AS day,
    COUNT(*) AS total_requests,
    SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) AS errors,
    ROUND(AVG(response_time_ms), 2) AS avg_rt_ms,
    ROUND(MAX(response_time_ms), 2) AS max_rt_ms
FROM web_logs
GROUP BY day
ORDER BY day;

-- ------------------------------------------------------------
-- 2. Top 10 slowest endpoints (by average response time)
-- ------------------------------------------------------------
SELECT
    path,
    COUNT(*) AS hits,
    ROUND(AVG(response_time_ms), 2) AS avg_rt,
    ROUND(MAX(response_time_ms), 2) AS max_rt,
    ROUND(SUM(response_time_ms) * 1.0 / COUNT(*), 2) AS weighted_avg
FROM web_logs
GROUP BY path
HAVING hits > 5
ORDER BY avg_rt DESC
LIMIT 10;

-- ------------------------------------------------------------
-- 3. Error rate by hour (hourly error percentage)
-- ------------------------------------------------------------
SELECT
    strftime('%Y-%m-%d %H:00:00', log_timestamp) AS hour,
    COUNT(*) AS total,
    SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) AS errors,
    ROUND(SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS error_pct
FROM web_logs
GROUP BY hour
ORDER BY hour;

-- ------------------------------------------------------------
-- 4. Response time percentiles (P50, P95, P99)
-- ------------------------------------------------------------
WITH ordered_rt AS (
    SELECT
        response_time_ms,
        ROW_NUMBER() OVER (ORDER BY response_time_ms) AS row_num,
        COUNT(*) OVER () AS total_count
    FROM web_logs
    WHERE response_time_ms IS NOT NULL
)
SELECT
    'P50' AS percentile,
    MIN(response_time_ms) AS value
FROM ordered_rt
WHERE row_num >= total_count * 0.50
UNION
SELECT
    'P95',
    MIN(response_time_ms)
FROM ordered_rt
WHERE row_num >= total_count * 0.95
UNION
SELECT
    'P99',
    MIN(response_time_ms)
FROM ordered_rt
WHERE row_num >= total_count * 0.99;

-- ------------------------------------------------------------
-- 5. Top client IPs by request count
-- ------------------------------------------------------------
SELECT
    client_ip,
    COUNT(*) AS requests,
    SUM(bytes_sent) AS total_bytes,
    ROUND(AVG(response_time_ms), 2) AS avg_rt
FROM web_logs
GROUP BY client_ip
ORDER BY requests DESC
LIMIT 10;

-- ------------------------------------------------------------
-- 6. Requests per HTTP method
-- ------------------------------------------------------------
SELECT
    method,
    COUNT(*) AS count,
    ROUND(AVG(response_time_ms), 2) AS avg_rt,
    SUM(bytes_sent) AS total_bytes
FROM web_logs
GROUP BY method
ORDER BY count DESC;

-- ------------------------------------------------------------
-- 7. Error types (by status code)
-- ------------------------------------------------------------
SELECT
    status_code,
    COUNT(*) AS count,
    ROUND(AVG(response_time_ms), 2) AS avg_rt
FROM web_logs
WHERE status_code >= 400
GROUP BY status_code
ORDER BY count DESC;

-- ------------------------------------------------------------
-- 8. Daily traffic trend with moving average (7-day)
-- ------------------------------------------------------------
WITH daily_traffic AS (
    SELECT
        DATE(log_timestamp) AS day,
        COUNT(*) AS requests
    FROM web_logs
    GROUP BY day
)
SELECT
    day,
    requests,
    ROUND(AVG(requests) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS moving_avg_7d
FROM daily_traffic
ORDER BY day;

-- ------------------------------------------------------------
-- 9. Peak traffic hours (day of week analysis)
-- ------------------------------------------------------------
SELECT
    strftime('%w', log_timestamp) AS day_of_week,
    strftime('%H', log_timestamp) AS hour,
    COUNT(*) AS requests
FROM web_logs
GROUP BY day_of_week, hour
ORDER BY day_of_week, hour;

-- ------------------------------------------------------------
-- 10. Users with high error rates (by client IP)
-- ------------------------------------------------------------
SELECT
    client_ip,
    COUNT(*) AS total_requests,
    SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) AS errors,
    ROUND(SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS error_pct
FROM web_logs
GROUP BY client_ip
HAVING total_requests > 10
ORDER BY error_pct DESC
LIMIT 10;

-- ------------------------------------------------------------
-- 11. Most popular referer URLs
-- ------------------------------------------------------------
SELECT
    referer,
    COUNT(*) AS count
FROM web_logs
WHERE referer != ''
GROUP BY referer
ORDER BY count DESC
LIMIT 10;

-- ------------------------------------------------------------
-- 12. Response time distribution (bucketed)
-- ------------------------------------------------------------
SELECT
    CASE
        WHEN response_time_ms < 100 THEN '0-100ms'
        WHEN response_time_ms < 300 THEN '100-300ms'
        WHEN response_time_ms < 500 THEN '300-500ms'
        WHEN response_time_ms < 1000 THEN '500-1000ms'
        ELSE '>1000ms'
    END AS bucket,
    COUNT(*) AS count
FROM web_logs
WHERE response_time_ms IS NOT NULL
GROUP BY bucket
ORDER BY bucket;

-- ------------------------------------------------------------
-- 13. Error log analysis (counts by level and source)
-- ------------------------------------------------------------
SELECT
    level,
    source,
    COUNT(*) AS count
FROM error_logs
GROUP BY level, source
ORDER BY count DESC;

-- ------------------------------------------------------------
-- 14. Recent errors (last 7 days)
-- ------------------------------------------------------------
SELECT
    error_timestamp,
    level,
    source,
    message
FROM error_logs
WHERE error_timestamp >= DATE('now', '-7 days')
ORDER BY error_timestamp DESC
LIMIT 20;

-- ------------------------------------------------------------
-- 15. Correlation between high response times and errors
-- ------------------------------------------------------------
SELECT
    CASE
        WHEN response_time_ms > 500 THEN 'Slow (>500ms)'
        ELSE 'Normal (<=500ms)'
    END AS response_category,
    COUNT(*) AS total_requests,
    SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) AS errors,
    ROUND(SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS error_pct
FROM web_logs
GROUP BY response_category;
