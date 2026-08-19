# Changelog for Employee Similarity & Mentor Recommender

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

- **Employee Similarity & Mentor Recommender** – Content‑based recommendation system for employee similarity.

  **Data Loading**:
  - Connect to `employees.db` using `sqlite3`
  - Load `employees` table

  **Feature Engineering**:
  - One‑hot encoding for `job_title` and `department`
  - Standard scaling for `salary` and `years_exp`
  - Feature matrix construction

  **Recommendation Algorithm**:
  - Cosine similarity between feature vectors
  - Top N most similar employees
  - Exclude self from recommendations
  - Random employee selection for demonstration

  **Analytical Features**:
  - Most similar pair identification
  - Department distribution analysis
  - Salary distribution analysis

  **Visualizations**:
  - Department distribution (bar chart)
  - Salary distribution (histogram)
  - Recommendations (horizontal bar chart)
  - Similarity heatmap (heatmap)

  **Technical Implementation**:
  - Python 3.8+ compatible
  - Modular code: `db_loader.py`, `recommender.py`, `visualizer.py`
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
