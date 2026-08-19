"""
visualizer.py – Plotting functions for employee similarity.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def set_style():
    sns.set_style("whitegrid")
    sns.set_palette("viridis")

def plot_department_distribution(df: pd.DataFrame):
    """Bar chart of employees per department."""
    set_style()
    dept_counts = df['department'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(dept_counts.index, dept_counts.values, color='steelblue')
    ax.set_title('Employees by Department', fontsize=16)
    ax.set_xlabel('Department')
    ax.set_ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_salary_distribution(df: pd.DataFrame):
    """Histogram of salaries."""
    set_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df['salary'], bins=20, color='coral', edgecolor='black', alpha=0.7)
    ax.set_title('Salary Distribution', fontsize=16)
    ax.set_xlabel('Salary ($)')
    ax.set_ylabel('Frequency')
    return fig

def plot_recommendations(rec_df: pd.DataFrame, title="Similar Employees"):
    """Horizontal bar chart of similarity scores."""
    set_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(rec_df['name'] + ' (' + rec_df['department'] + ')', rec_df['similarity'], color='lightgreen')
    ax.set_title(title, fontsize=16)
    ax.set_xlabel('Cosine Similarity')
    ax.set_ylabel('Employee')
    ax.invert_yaxis()
    plt.tight_layout()
    return fig

def plot_similarity_heatmap(similarity_matrix: np.ndarray, names: list, top_n: int = 10):
    """Heatmap of similarity for top N employees."""
    set_style()
    n = min(top_n, len(names))
    sub_sim = similarity_matrix[:n, :n]
    labels = names[:n]
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(sub_sim, ax=ax, xticklabels=labels, yticklabels=labels,
                cmap='coolwarm', annot=True, fmt='.2f')
    ax.set_title('Employee Similarity Heatmap (first N)', fontsize=16)
    plt.tight_layout()
    return fig
