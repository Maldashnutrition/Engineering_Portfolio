-- ============================================================
-- Log Analysis – Sample Data (Corrected, Working)
-- ============================================================

-- Clear existing data (if any)
DELETE FROM web_logs;
DELETE FROM error_logs;

-- ------------------------------------------------------------
-- Explicit logs for Jan 1-2 (already working)
-- ------------------------------------------------------------
INSERT INTO web_logs (log_timestamp, client_ip, method, path, status_code, bytes_sent, response_time_ms, user_agent, referer) VALUES
    ('2024-01-01 08:15:23', '192.168.1.100', 'GET', '/api/users', 200, 2048, 120, 'Mozilla/5.0', 'https://example.com'),
    ('2024-01-01 08:16:45', '192.168.1.101', 'GET', '/api/products', 200, 4096, 95, 'Chrome/120', 'https://example.com/products'),
    ('2024-01-01 08:17:10', '192.168.1.102', 'POST', '/api/orders', 201, 512, 350, 'Mozilla/5.0', 'https://example.com/cart'),
    ('2024-01-01 09:00:01', '10.0.0.5', 'GET', '/api/users', 200, 2048, 150, 'PostmanRuntime/7.26.8', ''),
    ('2024-01-01 09:05:33', '10.0.0.6', 'GET', '/api/products', 404, 256, 45, 'curl/7.68.0', ''),
    ('2024-01-01 09:12:12', '192.168.1.103', 'GET', '/api/users', 200, 2048, 180, 'Mozilla/5.0', 'https://example.com/users'),
    ('2024-01-01 10:20:45', '192.168.1.104', 'GET', '/api/products', 200, 4096, 200, 'Chrome/120', ''),
    ('2024-01-01 10:22:00', '192.168.1.105', 'GET', '/api/orders', 500, 512, 400, 'Mozilla/5.0', 'https://example.com/orders'),
    ('2024-01-01 11:00:30', '10.0.0.7', 'POST', '/api/orders', 201, 512, 600, 'PostmanRuntime/7.26.8', ''),
    ('2024-01-01 11:05:22', '10.0.0.8', 'GET', '/api/users', 200, 2048, 110, 'curl/7.68.0', ''),
    ('2024-01-01 12:00:00', '192.168.1.106', 'GET', '/api/products', 200, 4096, 90, 'Mozilla/5.0', 'https://example.com'),
    ('2024-01-01 12:10:10', '192.168.1.107', 'GET', '/api/users', 404, 256, 30, 'Chrome/120', 'https://example.com/users'),
    ('2024-01-01 13:30:15', '10.0.0.9', 'GET', '/api/orders', 200, 512, 250, 'PostmanRuntime/7.26.8', ''),
    ('2024-01-01 14:00:00', '192.168.1.108', 'GET', '/api/users', 200, 2048, 160, 'Mozilla/5.0', 'https://example.com/users'),
    ('2024-01-01 14:05:20', '192.168.1.109', 'GET', '/api/products', 200, 4096, 105, 'Chrome/120', ''),
    ('2024-01-01 15:15:50', '192.168.1.110', 'POST', '/api/orders', 500, 512, 450, 'Mozilla/5.0', 'https://example.com/cart'),
    ('2024-01-01 16:00:10', '10.0.0.10', 'GET', '/api/users', 200, 2048, 130, 'curl/7.68.0', ''),
    ('2024-01-01 17:30:45', '192.168.1.111', 'GET', '/api/products', 200, 4096, 80, 'Mozilla/5.0', ''),
    ('2024-01-01 18:00:00', '192.168.1.112', 'GET', '/api/orders', 200, 512, 290, 'Chrome/120', 'https://example.com/orders'),
    ('2024-01-01 19:20:15', '10.0.0.11', 'GET', '/api/users', 404, 256, 25, 'PostmanRuntime/7.26.8', ''),
    ('2024-01-02 08:00:00', '192.168.1.100', 'GET', '/api/users', 200, 2048, 140, 'Mozilla/5.0', 'https://example.com'),
    ('2024-01-02 08:15:20', '192.168.1.101', 'GET', '/api/products', 200, 4096, 110, 'Chrome/120', ''),
    ('2024-01-02 09:00:10', '10.0.0.5', 'POST', '/api/orders', 201, 512, 320, 'PostmanRuntime/7.26.8', ''),
    ('2024-01-02 09:30:00', '192.168.1.102', 'GET', '/api/users', 500, 512, 420, 'Mozilla/5.0', 'https://example.com/users'),
    ('2024-01-02 10:10:10', '192.168.1.103', 'GET', '/api/products', 200, 4096, 95, 'Chrome/120', ''),
    ('2024-01-02 11:00:30', '10.0.0.6', 'GET', '/api/orders', 200, 512, 260, 'curl/7.68.0', ''),
    ('2024-01-02 12:00:00', '192.168.1.104', 'GET', '/api/users', 200, 2048, 150, 'Mozilla/5.0', ''),
    ('2024-01-02 13:15:45', '192.168.1.105', 'GET', '/api/products', 404, 256, 35, 'Chrome/120', 'https://example.com/products'),
    ('2024-01-02 14:00:20', '10.0.0.7', 'POST', '/api/orders', 201, 512, 580, 'PostmanRuntime/7.26.8', ''),
    ('2024-01-02 15:30:00', '192.168.1.106', 'GET', '/api/users', 200, 2048, 170, 'Mozilla/5.0', 'https://example.com/users'),
    ('2024-01-02 16:00:10', '192.168.1.107', 'GET', '/api/products', 200, 4096, 100, 'Chrome/120', ''),
    ('2024-01-02 17:20:20', '10.0.0.8', 'GET', '/api/orders', 500, 512, 380, 'curl/7.68.0', ''),
    ('2024-01-02 18:00:00', '192.168.1.108', 'GET', '/api/users', 200, 2048, 125, 'Mozilla/5.0', ''),
    ('2024-01-02 19:10:30', '192.168.1.109', 'GET', '/api/products', 200, 4096, 85, 'Chrome/120', 'https://example.com/products');

-- ------------------------------------------------------------
-- Generated logs for Jan 3-10 using safe random generation
-- ------------------------------------------------------------
WITH RECURSIVE gen AS (
    SELECT 1 AS i
    UNION ALL
    SELECT i + 1 FROM gen WHERE i < 150
)
INSERT INTO web_logs (log_timestamp, client_ip, method, path, status_code, bytes_sent, response_time_ms, user_agent, referer)
SELECT
    datetime('2024-01-03 08:00:00', '+' || (abs(random()) % 1440) || ' minutes'),  -- random minute offset
    '192.168.1.' || (100 + (abs(random()) % 20)),
    CASE (abs(random()) % 3)
        WHEN 0 THEN 'GET'
        WHEN 1 THEN 'POST'
        ELSE 'PUT'
    END,
    CASE (abs(random()) % 3)
        WHEN 0 THEN '/api/users'
        WHEN 1 THEN '/api/products'
        ELSE '/api/orders'
    END,
    CASE (abs(random()) % 10)
        WHEN 0 THEN 500
        WHEN 1 THEN 404
        ELSE 200
    END,
    (1024 + (abs(random()) % 4096)),
    (50 + (abs(random()) % 950)),
    CASE (abs(random()) % 3)
        WHEN 0 THEN 'Mozilla/5.0'
        WHEN 1 THEN 'Chrome/120'
        ELSE 'curl/7.68.0'
    END,
    CASE (abs(random()) % 4)
        WHEN 0 THEN 'https://example.com'
        WHEN 1 THEN 'https://example.com/products'
        WHEN 2 THEN 'https://example.com/users'
        ELSE ''
    END
FROM gen;

-- ------------------------------------------------------------
-- Error logs
-- ------------------------------------------------------------
INSERT INTO error_logs (error_timestamp, level, source, message, stack_trace) VALUES
    ('2024-01-01 10:22:00', 'ERROR', 'api', 'Database connection timeout', 'Traceback: ...'),
    ('2024-01-01 15:15:50', 'ERROR', 'api', 'Order processing failed: invalid payload', 'Traceback: ...'),
    ('2024-01-02 09:30:00', 'ERROR', 'api', 'User authentication failure', 'Traceback: ...'),
    ('2024-01-02 17:20:20', 'ERROR', 'api', 'Internal server error: null pointer', 'Traceback: ...'),
    ('2024-01-03 08:15:10', 'WARNING', 'cache', 'Cache miss for key user_123', ''),
    ('2024-01-03 12:00:00', 'INFO', 'scheduler', 'Daily report generated', ''),
    ('2024-01-03 14:30:00', 'ERROR', 'db', 'Deadlock detected', 'Traceback: ...');
