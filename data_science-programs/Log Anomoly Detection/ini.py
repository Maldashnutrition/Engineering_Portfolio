#!/usr/bin/env python3
"""
Log Anomaly Detection – Run EDA and detect anomalies using Isolation Forest.
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from db_loader import load_web_logs, load_error_logs
from visualizer import (
    plot_response_time_distribution,
    plot_status_code_distribution,
    plot_response_time_by_status,
    plot_hourly_traffic,
    plot_anomalies,
    plot_anomaly_counts_by_status,
)

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create features for anomaly detection.
    Adds: hour, day_of_week, is_error, log_bytes, etc.
    """
    df = df.copy()
    # Time features
    df['hour'] = df['log_timestamp'].dt.hour
    df['day_of_week'] = df['log_timestamp'].dt.dayofweek  # Mon=0, Sun=6
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # Response time log transform (to handle skew)
    df['log_response_time'] = np.log1p(df['response_time_ms'])
    
    # Error flag
    df['is_error'] = (df['status_code'] >= 400).astype(int)
    
    # Bytes sent log transform
    df['log_bytes'] = np.log1p(df['bytes_sent'].fillna(0))
    
    # Path popularity (count of each path)
    path_counts = df['path'].value_counts()
    df['path_popularity'] = df['path'].map(path_counts)
    
    # Hourly error rate (percentage of errors in that hour)
    # We'll compute per hour: (errors in hour) / (total requests in hour)
    hourly_error_rate = df.groupby('hour')['is_error'].mean()
    df['hourly_error_rate'] = df['hour'].map(hourly_error_rate)
    
    return df

def detect_anomalies(df: pd.DataFrame, contamination: float = 0.1) -> pd.DataFrame:
    """
    Use Isolation Forest to detect anomalies.
    Returns DataFrame with 'anomaly' column (1=anomaly, 0=normal).
    """
    # Select features for model
    feature_cols = [
        'log_response_time', 
        'is_error', 
        'log_bytes', 
        'path_popularity', 
        'hourly_error_rate',
        'hour',
        'day_of_week'
    ]
    X = df[feature_cols].fillna(0)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Isolation Forest
    model = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=100
    )
    preds = model.fit_predict(X_scaled)
    # Isolation Forest returns 1 for inliers, -1 for outliers
    df['anomaly'] = (preds == -1).astype(int)
    
    return df

def main():
    print("Loading log data from logs.db...")
    logs_df = load_web_logs()
    error_df = load_error_logs()
    
    print(f"Loaded {len(logs_df)} web log records")
    print(f"Date range: {logs_df['log_timestamp'].min()} to {logs_df['log_timestamp'].max()}")
    
    print("\nEngineering features...")
    logs_df = engineer_features(logs_df)
    
    print("Detecting anomalies with Isolation Forest...")
    logs_df = detect_anomalies(logs_df, contamination=0.1)
    
    anomaly_count = logs_df['anomaly'].sum()
    print(f"Found {anomaly_count} anomalies ({anomaly_count/len(logs_df)*100:.1f}%)")
    
    print("\nGenerating plots...")
    
    # 1. Response time distribution
    fig = plot_response_time_distribution(logs_df)
    fig.savefig(OUTPUT_DIR / 'response_time_dist.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    # 2. Status code distribution
    fig = plot_status_code_distribution(logs_df)
    fig.savefig(OUTPUT_DIR / 'status_code_dist.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    # 3. Response time by status
    fig = plot_response_time_by_status(logs_df)
    fig.savefig(OUTPUT_DIR / 'response_time_by_status.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    # 4. Hourly traffic
    fig = plot_hourly_traffic(logs_df)
    fig.savefig(OUTPUT_DIR / 'hourly_traffic.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    # 5. Anomalies over time
    fig = plot_anomalies(logs_df)
    fig.savefig(OUTPUT_DIR / 'anomalies_over_time.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    # 6. Anomaly counts by status
    fig = plot_anomaly_counts_by_status(logs_df)
    fig.savefig(OUTPUT_DIR / 'anomalies_by_status.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    print(f"\nPlots saved to {OUTPUT_DIR}")
    
    # Summary statistics
    print("\n=== Summary Statistics ===")
    print(f"Total requests: {len(logs_df)}")
    print(f"Total errors (status >= 400): {logs_df['is_error'].sum()}")
    print(f"Error rate: {logs_df['is_error'].mean()*100:.2f}%")
    print(f"Average response time: {logs_df['response_time_ms'].mean():.2f} ms")
    print(f"Median response time: {logs_df['response_time_ms'].median():.2f} ms")
    print(f"Max response time: {logs_df['response_time_ms'].max():.2f} ms")
    print(f"Anomalies detected: {anomaly_count} ({anomaly_count/len(logs_df)*100:.1f}%)")
    
    # Top anomalous endpoints
    top_anomaly_paths = logs_df[logs_df['anomaly'] == 1]['path'].value_counts().head(5)
    if not top_anomaly_paths.empty:
        print("\nTop 5 anomalous endpoints:")
        for path, count in top_anomaly_paths.items():
            print(f"  {path}: {count} anomalies")
    
    # Save anomaly data
    anomaly_df = logs_df[logs_df['anomaly'] == 1]
    anomaly_df.to_csv(OUTPUT_DIR / 'anomalies.csv', index=False)
    print(f"\nAnomaly data saved to {OUTPUT_DIR / 'anomalies.csv'}")

if __name__ == "__main__":
    main()
