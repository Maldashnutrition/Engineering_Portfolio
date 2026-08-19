#!/usr/bin/env python3
"""
run_analysis.py – Run the full EDA and save plots.
"""

import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Import only load_all (load_joined_data is not used)
from db_loader import load_all
from visualizer import (
    plot_monthly_loans,
    plot_most_borrowed_books,
    plot_genre_distribution,
    plot_active_members_vs_inactive,
    plot_overdue_rate_by_month,
    plot_fines_distribution,
    plot_membership_type_distribution,
)

# Output directory for plots
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def main():
    print("Loading data from library.db...")
    data = load_all()
    loans_df = data['loans']
    books_df = data['books']
    members_df = data['members']
    fines_df = data['fines']

    # Convert date columns to datetime
    for col in ['loan_date', 'due_date', 'return_date']:
        loans_df[col] = pd.to_datetime(loans_df[col], errors='coerce')
    members_df['joined_date'] = pd.to_datetime(members_df['joined_date'], errors='coerce')

    # Merge loans with books and members for analysis
    joined = loans_df.merge(books_df, left_on='book_id', right_on='id') \
                     .merge(members_df, left_on='member_id', right_on='id', suffixes=('_book', '_member'))

    print("Generating plots...")

    # 1. Monthly loans
    fig = plot_monthly_loans(loans_df)
    fig.savefig(OUTPUT_DIR / 'monthly_loans.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # 2. Most borrowed books
    fig = plot_most_borrowed_books(joined, top_n=10)
    fig.savefig(OUTPUT_DIR / 'most_borrowed_books.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # 3. Genre distribution
    fig = plot_genre_distribution(joined)
    fig.savefig(OUTPUT_DIR / 'genre_distribution.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # 4. Active vs inactive members
    fig = plot_active_members_vs_inactive(members_df)
    fig.savefig(OUTPUT_DIR / 'member_status.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # 5. Overdue rate by month
    fig = plot_overdue_rate_by_month(loans_df)
    fig.savefig(OUTPUT_DIR / 'overdue_rate.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # 6. Fines distribution
    fig = plot_fines_distribution(fines_df)
    fig.savefig(OUTPUT_DIR / 'fines_distribution.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # 7. Membership type distribution
    fig = plot_membership_type_distribution(members_df)
    fig.savefig(OUTPUT_DIR / 'membership_types.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    print("Plots saved to", OUTPUT_DIR)

    # Summary statistics
    print("\n=== Summary Statistics ===")
    print(f"Total books: {len(books_df)}")
    print(f"Total members: {len(members_df)}")
    print(f"Total loans: {len(loans_df)}")
    print(f"Total fines: {len(fines_df)}")
    print(f"Active members: {members_df['is_active'].sum()}")
    print(f"Overdue loans: {len(loans_df[loans_df['status'] == 'overdue'])}")

    # Most popular genre
    top_genre = joined['genre'].value_counts().idxmax()
    print(f"Most popular genre: {top_genre}")

    # Most borrowed book
    top_book = joined['title'].value_counts().idxmax()
    print(f"Most borrowed book: {top_book}")

if __name__ == "__main__":
    main()
