-- ============================================================
-- Log Analysis – Database Schema
-- SQLite 3.x compatible
-- ============================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- Table: web_logs (raw logs – parsed fields)
-- ------------------------------------------------------------
CREATE TABLE web_logs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    log_timestamp   DATETIME NOT NULL,
    client_ip       TEXT NOT NULL,
    method          TEXT NOT NULL,      -- GET, POST, etc.
    path            TEXT NOT NULL,      -- URL path
    status_code     INTEGER NOT NULL,
    bytes_sent      INTEGER,
    response_time_ms INTEGER,           -- response time in milliseconds
    user_agent      TEXT,
    referer         TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Table: error_logs (optional, for parsing error logs)
-- ------------------------------------------------------------
CREATE TABLE error_logs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    error_timestamp DATETIME NOT NULL,
    level           TEXT NOT NULL,      -- ERROR, WARNING, INFO, etc.
    source          TEXT,               -- module/component
    message         TEXT NOT NULL,
    stack_trace     TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Indexes for performance
-- ------------------------------------------------------------
CREATE INDEX idx_web_logs_timestamp ON web_logs(log_timestamp);
CREATE INDEX idx_web_logs_path ON web_logs(path);
CREATE INDEX idx_web_logs_status ON web_logs(status_code);
CREATE INDEX idx_web_logs_method ON web_logs(method);
CREATE INDEX idx_web_logs_client_ip ON web_logs(client_ip);

CREATE INDEX idx_error_logs_timestamp ON error_logs(error_timestamp);
CREATE INDEX idx_error_logs_level ON error_logs(level);

-- ------------------------------------------------------------
-- Views
-- ------------------------------------------------------------

-- View: hourly summary
CREATE VIEW v_hourly_summary AS
SELECT
    strftime('%Y-%m-%d %H:00:00', log_timestamp) AS hour,
    COUNT(*) AS total_requests,
    SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) AS error_count,
    ROUND(AVG(response_time_ms), 2) AS avg_response_ms,
    ROUND(MAX(response_time_ms), 2) AS max_response_ms,
    ROUND(MIN(response_time_ms), 2) AS min_response_ms,
    SUM(bytes_sent) AS total_bytes
FROM web_logs
GROUP BY hour
ORDER BY hour;

-- View: top slowest endpoints
CREATE VIEW v_slowest_endpoints AS
SELECT
    path,
    COUNT(*) AS hit_count,
    ROUND(AVG(response_time_ms), 2) AS avg_response_ms,
    ROUND(MAX(response_time_ms), 2) AS max_response_ms,
    ROUND(PERCENTILE(response_time_ms, 95), 2) AS p95_response_ms
FROM web_logs
GROUP BY path
HAVING hit_count > 10
ORDER BY p95_response_ms DESC;
