# Log Analysis & Performance Monitoring

A SQL database project for analyzing web server logs, tracking performance metrics, and identifying errors. This project demonstrates time‑series analysis, percentiles, moving averages, and error rate monitoring – all built on SQLite.

---

## Overview

This system provides a complete log analysis platform:

- **Web Logs** – Track HTTP requests with timestamps, client IP, method, path, status code, response time, and bytes sent.
- **Error Logs** – Track application errors with timestamps, severity level, source, and message.
- **Analytical Queries** – Response time percentiles, error rates, hourly traffic patterns, and performance trends.

### Key Features

- **Time‑series analysis** with hourly/daily aggregation
- **Percentile calculations** (P50, P95, P99) for performance monitoring
- **Moving averages** for trend detection
- **Error rate analysis** by hour, endpoint, and client
- **Correlation analysis** between slow responses and errors

---

## Schema

The database consists of two core tables:

| Table | Purpose |
|-------|---------|
| `web_logs` | HTTP request logs with timestamps, status codes, response times |
| `error_logs` | Application error logs with severity levels and messages |


## Installation

1. Ensure you have SQLite 3.x and Python 3.6+ installed.
2. Copy `logs.db` (or create it via `make init` and `make seed`).
3. Python wrapper uses only the standard library – no external dependencies.

---

## Usage

### Initialize the Database

```bash
make init
