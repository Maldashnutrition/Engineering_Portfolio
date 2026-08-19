"""
visualizer.py – Plotting functions for sales analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def set_style():
    sns.set_style("whitegrid")
    sns.set_palette("viridis")

def plot_monthly_revenue(sales_df: pd.DataFrame):
    """Plot monthly revenue trend."""
    set_style()
    sales_df = sales_df.copy()
    sales_df['month'] = sales_df['full_date'].dt.to_period('M')
    monthly = sales_df.groupby('month')['revenue'].sum().reset_index()
    monthly['month'] = monthly['month'].astype(str)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(monthly['month'], monthly['revenue'], color='steelblue')
    ax.set_title('Monthly Revenue', fontsize=16)
    ax.set_xlabel('Month')
    ax.set_ylabel('Revenue ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_top_products(sales_df: pd.DataFrame, top_n: int = 10):
    """Plot top N products by revenue."""
    set_style()
    top = sales_df.groupby('product_id')['revenue'].sum().sort_values(ascending=False).head(top_n)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    top.plot(kind='bar', ax=ax, color='coral')
    ax.set_title(f'Top {top_n} Products by Revenue', fontsize=16)
    ax.set_xlabel('Product ID')
    ax.set_ylabel('Revenue ($)')
    plt.xticks(rotation=0)
    plt.tight_layout()
    return fig

def plot_weekly_pattern(sales_df: pd.DataFrame):
    """Plot revenue by day of week."""
    set_style()
    weekly = sales_df.groupby('day_name')['revenue'].sum().reset_index()
    # Order days correctly
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly['day_name'] = pd.Categorical(weekly['day_name'], categories=day_order, ordered=True)
    weekly = weekly.sort_values('day_name')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(weekly['day_name'], weekly['revenue'], color='lightgreen')
    ax.set_title('Revenue by Day of Week', fontsize=16)
    ax.set_xlabel('Day')
    ax.set_ylabel('Revenue ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_revenue_trend(sales_df: pd.DataFrame):
    """Plot daily revenue trend line."""
    set_style()
    daily = sales_df.groupby('full_date')['revenue'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(daily['full_date'], daily['revenue'], color='teal', linewidth=1.5)
    ax.set_title('Daily Revenue Trend', fontsize=16)
    ax.set_xlabel('Date')
    ax.set_ylabel('Revenue ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_forecast(forecast_df: pd.DataFrame):
    """Plot forecast with confidence intervals."""
    set_style()
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Historical data
    hist = forecast_df[forecast_df['yhat'].notna()]
    ax.plot(hist['ds'], hist['yhat'], color='teal', linewidth=2, label='Historical')
    
    # Forecast
    future = forecast_df[forecast_df['yhat'].notna() == False]
    ax.plot(future['ds'], future['yhat'], color='orange', linewidth=2, label='Forecast')
    ax.fill_between(
        future['ds'],
        future['yhat_lower'],
        future['yhat_upper'],
        color='orange',
        alpha=0.2,
        label='Confidence Interval'
    )
    
    ax.axvline(x=hist['ds'].max(), color='red', linestyle='--', alpha=0.5, label='Forecast Start')
    ax.set_title('Revenue Forecast', fontsize=16)
    ax.set_xlabel('Date')
    ax.set_ylabel('Revenue ($)')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig
