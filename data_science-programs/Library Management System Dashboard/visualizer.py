"""
visualizer.py – Plotting functions for library analytics.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def set_style():
    """Set consistent plot style."""
    sns.set_style("whitegrid")
    sns.set_palette("viridis")

def plot_monthly_loans(loans_df: pd.DataFrame):
    """
    Plot monthly loan trend.
    loans_df must have a 'loan_date' column (datetime).
    """
    set_style()
    loans_df = loans_df.copy()
    loans_df['month'] = loans_df['loan_date'].dt.to_period('M')
    monthly = loans_df.groupby('month').size()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    monthly.plot(kind='line', marker='o', ax=ax, color='teal')
    ax.set_title('Monthly Loan Trends', fontsize=16)
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Loans')
    ax.grid(True)
    return fig

def plot_most_borrowed_books(loans_df: pd.DataFrame, top_n: int = 10):
    """
    Plot top N most borrowed books.
    loans_df must have a 'title' column.
    """
    set_style()
    top_books = loans_df['title'].value_counts().head(top_n)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    top_books.plot(kind='bar', ax=ax, color='coral')
    ax.set_title(f'Top {top_n} Most Borrowed Books', fontsize=16)
    ax.set_xlabel('Book Title')
    ax.set_ylabel('Number of Loans')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

def plot_genre_distribution(loans_df: pd.DataFrame):
    """
    Plot loan distribution by genre.
    loans_df must have a 'genre' column.
    """
    set_style()
    genre_counts = loans_df['genre'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    genre_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=90,
                      colors=sns.color_palette("Set3", len(genre_counts)))
    ax.set_ylabel('')
    ax.set_title('Loans by Genre', fontsize=16)
    return fig

def plot_active_members_vs_inactive(members_df: pd.DataFrame):
    """
    Pie chart of active vs inactive members.
    members_df must have 'is_active' column (0/1).
    """
    set_style()
    counts = members_df['is_active'].value_counts()
    labels = ['Active' if v == 1 else 'Inactive' for v in counts.index]
    
    fig, ax = plt.subplots(figsize=(8, 8))
    counts.plot(kind='pie', labels=labels, autopct='%1.1f%%', ax=ax,
                colors=['lightgreen', 'lightcoral'], startangle=90)
    ax.set_title('Member Status', fontsize=16)
    ax.set_ylabel('')
    return fig

def plot_overdue_rate_by_month(loans_df: pd.DataFrame):
    """
    Plot monthly overdue rate (percentage of loans that were overdue).
    loans_df must have 'loan_date', 'status', and 'return_date'.
    """
    set_style()
    loans_df = loans_df.copy()
    loans_df['month'] = loans_df['loan_date'].dt.to_period('M')
    # Compute overdue flag: status == 'overdue' OR return_date > due_date
    loans_df['overdue'] = (loans_df['status'] == 'overdue') | \
                          (loans_df['return_date'] > loans_df['due_date'])
    # Use 'id' as the primary key column (not 'loan_id')
    monthly = loans_df.groupby('month').agg(
        total=('id', 'count'),
        overdue=('overdue', 'sum')
    )
    monthly['overdue_pct'] = monthly['overdue'] / monthly['total'] * 100
    
    fig, ax = plt.subplots(figsize=(12, 6))
    monthly['overdue_pct'].plot(kind='bar', ax=ax, color='salmon')
    ax.set_title('Monthly Overdue Rate (%)', fontsize=16)
    ax.set_xlabel('Month')
    ax.set_ylabel('Overdue Percentage')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_fines_distribution(fines_df: pd.DataFrame):
    """
    Histogram of fine amounts.
    fines_df must have 'amount' column.
    """
    set_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(fines_df['amount'], bins=20, color='goldenrod', edgecolor='black', alpha=0.7)
    ax.set_title('Distribution of Fine Amounts', fontsize=16)
    ax.set_xlabel('Fine Amount ($)')
    ax.set_ylabel('Frequency')
    return fig

def plot_membership_type_distribution(members_df: pd.DataFrame):
    """
    Count of members by membership type.
    """
    set_style()
    counts = members_df['membership_type'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    counts.plot(kind='bar', ax=ax, color=['#66b3ff', '#ff9999', '#99ff99'])
    ax.set_title('Membership Types', fontsize=16)
    ax.set_xlabel('Membership Type')
    ax.set_ylabel('Number of Members')
    plt.xticks(rotation=0)
    return fig
