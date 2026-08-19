#!/usr/bin/env python3
"""
Sales Forecast Analysis – Run EDA and generate forecast (if Prophet available).
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from db_loader import load_sales_data, load_daily_revenue
from visualizer import (
    plot_monthly_revenue,
    plot_top_products,
    plot_weekly_pattern,
    plot_revenue_trend,
    plot_forecast,
)

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def main():
    print("Loading sales data from sales.db...")
    sales_df = load_sales_data()
    daily_df = load_daily_revenue()
    
    print(f"Loaded {len(sales_df)} sales records")
    print(f"Date range: {sales_df['full_date'].min()} to {sales_df['full_date'].max()}")
    
    print("\nGenerating plots...")
    
    # 1. Monthly revenue
    fig = plot_monthly_revenue(sales_df)
    fig.savefig(OUTPUT_DIR / 'monthly_revenue.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    # 2. Top products
    fig = plot_top_products(sales_df, top_n=10)
    fig.savefig(OUTPUT_DIR / 'top_products.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    # 3. Weekly pattern
    fig = plot_weekly_pattern(sales_df)
    fig.savefig(OUTPUT_DIR / 'weekly_pattern.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    # 4. Revenue trend
    fig = plot_revenue_trend(sales_df)
    fig.savefig(OUTPUT_DIR / 'revenue_trend.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    # 5. Forecast (only if Prophet is available and works)
    try:
        from prophet import Prophet
        
        print("\nBuilding Prophet forecast...")
        model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
        model.fit(daily_df)
        future = model.make_future_dataframe(periods=90)
        forecast = model.predict(future)
        
        fig = plot_forecast(forecast)
        fig.savefig(OUTPUT_DIR / 'forecast.png', dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        forecast.to_csv(OUTPUT_DIR / 'forecast_data.csv', index=False)
        print(f"Forecast saved to {OUTPUT_DIR / 'forecast_data.csv'}")
    except ImportError:
        print("Prophet not installed. Skipping forecast.")
    except AttributeError as e:
        print(f"Prophet compatibility issue: {e}. Skipping forecast.")
    except Exception as e:
        print(f"Forecast failed: {e}. Skipping forecast.")
    
    print(f"\nPlots saved to {OUTPUT_DIR}")
    
    # Summary statistics
    print("\n=== Summary Statistics ===")
    print(f"Total revenue: ${sales_df['revenue'].sum():,.2f}")
    print(f"Total sales: {len(sales_df)}")
    print(f"Unique products: {sales_df['product_id'].nunique()}")
    print(f"Unique stores: {sales_df['store_id'].nunique()}")
    print(f"Unique customers: {sales_df['customer_id'].nunique()}")
    
    # Monthly stats
    sales_df['month'] = sales_df['full_date'].dt.to_period('M')
    monthly = sales_df.groupby('month')['revenue'].sum()
    print(f"\nBest month: {monthly.idxmax()} (${monthly.max():,.2f})")
    print(f"Worst month: {monthly.idxmin()} (${monthly.min():,.2f})")
    print(f"Average monthly revenue: ${monthly.mean():,.2f}")

if __name__ == "__main__":
    main()
