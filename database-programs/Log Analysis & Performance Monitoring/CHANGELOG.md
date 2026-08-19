# Changelog for Log Analysis & Performance Monitoring

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned

- None currently.

---

## [1.0.0] – 2026-08-16

### Added

- **Log Analysis & Performance Monitoring** – SQL database for analyzing web server logs.

  **Schema**:
  - `web_logs` – HTTP request logs with timestamp, IP, method, path, status, bytes, response time
  - `error_logs` – Application error logs with timestamp, level, source, message, stack trace
  - Indexes on `log_timestamp`, `path`, `status_code`, `client_ip`, `response_time_ms`

  **Views**:
  - `v_hourly_summary` – Hourly aggregates (requests, errors, avg/max response time)
  - `v_slowest_endpoints` – Endpoints ranked by P95 response time

  **Analytical Queries**:
  - Total requests, errors, avg/max response time per day
  - Top 10 slowest endpoints by average response time
  - Hourly error rate percentage
  - Response time percentiles (P50, P95, P99)
  - Top client IPs by request count
  - Requests per HTTP method
  - Daily traffic trend with 7‑day moving average
  - Peak traffic hours (day of week + hour)
  - Users with high error rates (by client IP)
  - Most popular referer URLs
  - Response time distribution (bucketed)
  - Error log analysis by level and source
  - Correlation between high response times and errors

  **CLI Wrapper** (`ini.py`):
  - `make init` – Create database schema
  - `make seed` – Load sample data
  - `make reset` – Delete and recreate database
  - `make query SQL="..."` – Run custom SQL queries
  - `make interactive` – Interactive SQL shell
  - `make all` – Run all pre‑defined analytical queries
  - `make list` – List all available queries

  **Sample Data**:
  - 184 web log records from 2024‑01‑01 to 2024‑01‑04
  - Multiple HTTP methods (GET, POST, PUT)
  - Realistic status codes (200, 404, 500)
  - Response times ranging from 25ms to 1200ms
  - 7 error log records with various severity levels

### Fixed

- N/A (initial release)

### Security

- Parameterized queries prevent SQL injection
- No authentication required (local use only)

---

## [0.1.0] – 2026-08-15

### Added

- Initial prototype (not publicly released)

---

[1.0.0]: https://github.com/[your-username]/[repo-name]/releases/tag/v1.0.0
