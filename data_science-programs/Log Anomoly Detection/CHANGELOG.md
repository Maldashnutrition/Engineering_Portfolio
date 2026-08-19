# Changelog for Log Anomaly Detection

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

- **Log Anomaly Detection** – Unsupervised anomaly detection for web logs using Isolation Forest.

  **Data Loading**:
  - Connect to `logs.db` using `sqlite3`
  - Load `web_logs` and `error_logs` tables

  **Feature Engineering**:
  - Hour of day
  - Day of week
  - Weekend flag
  - Log‑transformed response time (handles skew)
  - Error flag (status >= 400)
  - Log‑transformed bytes sent
  - Path popularity (request count per path)
  - Hourly error rate

  **Anomaly Detection**:
  - Isolation Forest with configurable contamination rate (default: 0.1)
  - StandardScaler for feature normalization
  - Anomaly flag (`anomaly` column)

  **Visualizations**:
  - Response time distribution (histogram)
  - Status code distribution (bar chart)
  - Response time by status code (box plot)
  - Hourly traffic (bar chart)
  - Anomalies over time (scatter plot)
  - Anomaly counts by status code (bar chart)

  **Technical Implementation**:
  - Python 3.8+ compatible
  - Modular code: `db_loader.py`, `visualizer.py`
  - Uses `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`
  - Makefile for automation: `install`, `run`, `clean`

### Fixed

- N/A (initial release)

### Security

- Read‑only access to database
- No system modifications
- Output written to `output/` folder only

---

## [0.1.0] – 2026-08-15

### Added

- Initial prototype (not publicly released)

---

[1.0.0]: https://github.com/[your-username]/[repo-name]/releases/tag/v1.0.0
