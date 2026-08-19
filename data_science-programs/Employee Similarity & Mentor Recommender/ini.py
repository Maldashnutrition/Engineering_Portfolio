#!/usr/bin/env python3
"""
Employee Similarity Recommender – Content-based.
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity   # <-- ADD THIS

from db_loader import load_employees, load_managers
from recommender import EmployeeRecommender
from visualizer import (
    plot_department_distribution,
    plot_salary_distribution,
    plot_recommendations,
    plot_similarity_heatmap,
)

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def main():
    print("Loading employee data from employees.db...")
    employees_df = load_employees()
    managers_df = load_managers()

    print(f"Loaded {len(employees_df)} employees.")
    print(f"Columns: {employees_df.columns.tolist()}")

    # Basic EDA
    print("\nDepartment distribution:")
    print(employees_df['department'].value_counts())

    # Build recommender
    recommender = EmployeeRecommender(employees_df)

    # 1. Find most similar pair
    emp1, emp2, sim = recommender.most_similar_pair()
    print(f"\nMost similar pair: {emp1} and {emp2} (similarity: {sim:.3f})")

    # 2. Recommendations for a random employee
    emp_id, recs = recommender.recommend_random(top_n=5)
    print(f"\nRecommendations for Employee {emp_id}:")
    print(recs[['name', 'job_title', 'department', 'similarity']])

    # 3. Generate plots
    print("\nGenerating plots...")

    fig = plot_department_distribution(employees_df)
    fig.savefig(OUTPUT_DIR / 'department_distribution.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    fig = plot_salary_distribution(employees_df)
    fig.savefig(OUTPUT_DIR / 'salary_distribution.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    if not recs.empty:
        fig = plot_recommendations(recs, title=f"Similar Employees for {employees_df.loc[employees_df['id']==emp_id, 'name'].iloc[0]}")
        fig.savefig(OUTPUT_DIR / 'recommendations.png', dpi=150, bbox_inches='tight')
        plt.close(fig)

    # Similarity heatmap (first 10 employees)
    all_sim = cosine_similarity(recommender.feature_matrix)
    fig = plot_similarity_heatmap(all_sim, recommender.names[:10], top_n=10)
    fig.savefig(OUTPUT_DIR / 'similarity_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    print(f"Plots saved to {OUTPUT_DIR}")

    # Save recommendations to CSV
    if not recs.empty:
        recs.to_csv(OUTPUT_DIR / 'recommendations.csv', index=False)
        print(f"Recommendations saved to {OUTPUT_DIR / 'recommendations.csv'}")

    # Summary
    print("\n=== Summary ===")
    print(f"Total employees: {len(employees_df)}")
    print(f"Unique departments: {employees_df['department'].nunique()}")
    print(f"Unique job titles: {employees_df['job_title'].nunique()}")

if __name__ == "__main__":
    main()
