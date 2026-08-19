# Log Anomaly Detection

A machine learning project that detects anomalous web requests using Isolation Forest. This project demonstrates feature engineering, unsupervised anomaly detection, and performance monitoring – all built on Python with scikit-learn.

---

## Overview

This project analyzes web server logs to identify anomalous requests:

- **Feature engineering** – Extract time-based features, error rates, and path popularity.
- **Anomaly detection** – Use Isolation Forest to identify unusual requests.
- **Visualization** – Plot anomalies over time and by status code.
- **Analysis** – Identify problematic endpoints and error patterns.

### Key Features

- **Feature engineering** – Hour of day, day of week, error rate, path popularity, log-transformed response times.
- **Isolation Forest** – Unsupervised anomaly detection with configurable contamination rate.
- **Visualizations** – Response time distribution, status code distribution, anomalies over time.
- **Insight generation** – Top anomalous endpoints and error patterns.

---

## Installation

1. Ensure you have Python 3.8+ and `pip` installed.
2. Copy `logs.db` from the database project into this directory.
3. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
