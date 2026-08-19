"""
visualizer.py – Plotting functions for log anomaly detection.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def set_style():
    sns.set_style("whitegrid")
    sns.set_palette("viridis")

def plot_response_time_distribution(df: pd.DataFrame):
    """Histogram of response times."""
    set_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df['response_time_ms'].dropna(), bins=30, color='steelblue', edgecolor='black', alpha=0.7)
    ax.set_title('Response Time Distribution', fontsize=16)
    ax.set_xlabel('Response Time (ms)')
    ax.set_ylabel('Frequency')
    return fig

def plot_status_code_distribution(df: pd.DataFrame):
    """Bar chart of status codes."""
    set_style()
    counts = df['status_code'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(counts.index.astype(str), counts.values, color='coral')
    ax.set_title('Status Code Distribution', fontsize=16)
    ax.set_xlabel('Status Code')
    ax.set_ylabel('Count')
    return fig

def plot_response_time_by_status(df: pd.DataFrame):
    """Box plot of response time by status code."""
    set_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='status_code', y='response_time_ms', ax=ax)
    ax.set_title('Response Time by Status Code', fontsize=16)
    ax.set_xlabel('Status Code')
    ax.set_ylabel('Response Time (ms)')
    return fig

def plot_hourly_traffic(df: pd.DataFrame):
    """Hourly request count."""
    set_style()
    df = df.copy()
    df['hour'] = df['log_timestamp'].dt.hour
    hourly = df.groupby('hour').size()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(hourly.index, hourly.values, color='lightgreen')
    ax.set_title('Hourly Traffic', fontsize=16)
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Request Count')
    return fig

def plot_anomalies(df: pd.DataFrame, anomaly_col: str = 'anomaly'):
    """
    Plot response time over time with anomalies highlighted.
    df must have 'log_timestamp', 'response_time_ms', and anomaly_col (0/1).
    """
    set_style()
    fig, ax = plt.subplots(figsize=(14, 6))
    normal = df[df[anomaly_col] == 0]
    anomaly = df[df[anomaly_col] == 1]
    ax.scatter(normal['log_timestamp'], normal['response_time_ms'], 
               label='Normal', color='steelblue', alpha=0.5, s=10)
    ax.scatter(anomaly['log_timestamp'], anomaly['response_time_ms'], 
               label='Anomaly', color='red', s=30, marker='x')
    ax.set_title('Response Time with Anomalies Highlighted', fontsize=16)
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Response Time (ms)')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_anomaly_counts_by_status(df: pd.DataFrame, anomaly_col: str = 'anomaly'):
    """Bar chart of normal vs anomaly counts by status code."""
    set_style()
    # Count per status and anomaly status
    counts = df.groupby(['status_code', anomaly_col]).size().unstack(fill_value=0)
    counts.columns = ['Normal', 'Anomaly']
    fig, ax = plt.subplots(figsize=(10, 6))
    counts.plot(kind='bar', ax=ax, color=['steelblue', 'red'])
    ax.set_title('Normal vs Anomaly by Status Code', fontsize=16)
    ax.set_xlabel('Status Code')
    ax.set_ylabel('Count')
    ax.legend()
    plt.xticks(rotation=0)
    return fig
