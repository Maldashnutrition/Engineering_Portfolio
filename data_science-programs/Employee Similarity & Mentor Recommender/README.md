# Employee Similarity & Mentor Recommender

A content‑based recommendation system that finds similar employees based on job title, department, and salary. This project demonstrates feature engineering, cosine similarity, and recommendation generation – all built on Python with scikit-learn.

---

## Overview

This project analyzes employee data to recommend similar colleagues:

- **Feature engineering** – Encode job titles, departments, and scale numerical features.
- **Similarity computation** – Use cosine similarity to find similar employees.
- **Recommendation generation** – Suggest mentors, collaborators, or similar-role colleagues.
- **Visualization** – Heatmaps of similarity matrices and recommendation scores.

### Key Features

- **Content‑based filtering** – Recommendations based on employee attributes.
- **Feature engineering** – One‑hot encoding for categorical features, scaling for numerical features.
- **Cosine similarity** – Measure similarity between employees.
- **Visualizations** – Department distribution, salary distribution, similarity heatmap.

---

## Installation

1. Ensure you have Python 3.8+ and `pip` installed.
2. Copy `employees.db` from the database project into this directory.
3. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
