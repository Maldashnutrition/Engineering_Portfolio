Here is the **top-level README** for your entire repository – the "front door" to your portfolio.

Create `README.md` in the root of `git_profile/`:

```markdown
# Engineering Portfolio

> A curated collection of projects demonstrating systems engineering, database architecture, and data science – built from the ground up with professional-grade structure and documentation.

---

## Portfolio Overview

| Domain | Projects | Key Skills |
|--------|----------|------------|
| **Systems & Security** | 4 standalone patterns | Bash, Finite State Machines, Configuration Firewalls, Transactional Systems |
| **Database Architecture** | 4 SQL projects | Schema Design, Recursive CTEs, Star Schemas, Full-Text Search |
| **Data Science & Analytics** | 4 analysis projects | EDA, Time-Series Forecasting, Anomaly Detection, Recommendation Systems |

---

## Project Index

### 🛡️ Systems & Security

| Project | Description | Key Concept |
|---------|-------------|-------------|
| **FSM DNS Leak Detector** | State machine for detecting and auto-repairing DNS leaks | Finite State Machine, Incident Response |
| **OpenVPN Config Sanitizer** | Security-first parser that strips dangerous directives | Configuration Firewall, Allow/Block Lists |
| **Transactional Reverter** | Atomic system hardening with JSON-based rollback | Transactional Operations, Idempotency |
| **Idle Watchdog** | Traffic-aware scheduler that rotates only during idle periods | Predictive Heuristics, Traffic Monitoring |

---

### 🗄️ Database Architecture

| Project | Description | Key Concept |
|---------|-------------|-------------|
| **Library Management** | CRUD operations with business logic (triggers, views) | Schema Design, Triggers |
| **Employee Org Chart** | Hierarchical data traversal with recursive CTEs | Recursive CTEs, Tree Queries |
| **Sales Analytics** | Star schema for business intelligence reporting | Data Warehousing, Window Functions |
| **Log Analysis** | Performance monitoring with time-series analysis | Percentiles, Moving Averages |

---

### 📊 Data Science & Analytics

| Project | Description | Key Concept |
|---------|-------------|-------------|
| **Library Analytics Dashboard** | EDA and visualization of library borrowing patterns | EDA, Visualization |
| **Sales Forecasting** | Revenue forecasting with Prophet + Streamlit dashboard | Time-Series, Prophet |
| **Log Anomaly Detection** | Isolation Forest for detecting anomalous web requests | Unsupervised ML, Anomaly Detection |
| **Employee Recommender** | Content-based recommendation system for employee similarity | Collaborative Filtering, Cosine Similarity |

---

## Technical Stack

| Category | Technologies |
|----------|--------------|
| **Languages** | Python, Bash, SQL |
| **Databases** | SQLite |
| **Data Science** | Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, Prophet |
| **ML Models** | Isolation Forest, Cosine Similarity, Collaborative Filtering |
| **Tools** | Make, Git, Virtual Environments |
| **Documentation** | Markdown, Jupyter Notebooks |

---

## Why These Projects

Each project was designed to demonstrate a specific engineering principle:

| Principle | Project |
|-----------|---------|
| **Finite State Machines** | FSM DNS Leak Detector |
| **Configuration Security** | OpenVPN Config Sanitizer |
| **Atomic Operations** | Transactional Reverter |
| **Predictive Heuristics** | Idle Watchdog |
| **Schema Design** | Library Management |
| **Recursive Queries** | Employee Org Chart |
| **Data Warehousing** | Sales Analytics |
| **Time-Series Analysis** | Sales Forecasting |
| **Anomaly Detection** | Log Anomaly Detection |
| **Recommendation Systems** | Employee Recommender |

### Clone the Repository

```bash
git clone https://github.com/yourusername/engineering-portfolio.git
cd engineering-portfolio
```

### Run a Security Project (Example)

```bash
cd security-programs/fsm-leak-detector
make install
make run
```

### Run a Database Project (Example)

```bash
cd database-programs/Library\ Management\ System
make reset
make query SQL="SELECT * FROM books LIMIT 5;"
```

### Run a Data Science Project (Example)

```bash
cd data_science-programs/Library\ Management\ System\ Dashboard
make install
make run
```
---
