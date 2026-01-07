import pandas as pd
import numpy as np
from scipy import stats
from .config import (
    STATE_COL, DIST_COL, DATE_COL,
    AGE_0_5_COL, AGE_5_17_COL, AGE_18_PLUS_COL
)

def get_summary_stats(enrol, demo, bio):
    """Generate basic summary statistics."""
    summary = {
        'enrol_records': len(enrol),
        'demo_records': len(demo),
        'bio_records': len(bio),
        'date_range_enrol': f"{enrol[DATE_COL].min()} to {enrol[DATE_COL].max()}" if DATE_COL in enrol else "N/A",
        'unique_states': enrol[STATE_COL].nunique() if STATE_COL in enrol else 0,
        'unique_districts': enrol[DIST_COL].nunique() if DIST_COL in enrol else 0,
    }
    
    # Calculate total enrollments by age group
    if 'Total_Enrollments' in enrol.columns:
        summary['total_enrollments'] = int(enrol['Total_Enrollments'].sum())
    
    return summary

def state_wise_analysis(df):
    """Analyze enrollments by state."""
    if STATE_COL not in df.columns or 'Total_Enrollments' not in df.columns:
        return pd.DataFrame()
    
    state_stats = df.groupby(STATE_COL).agg({
        'Total_Enrollments': ['sum', 'mean', 'std'],
        DATE_COL: 'count'
    }).round(2)
    
    state_stats.columns = ['Total_Enrollments', 'Avg_per_Record', 'StdDev', 'Record_Count']
    state_stats = state_stats.sort_values('Total_Enrollments', ascending=False)
    
    return state_stats

def age_group_distribution(df):
    """Calculate percentage distribution across age groups."""
    age_cols = [AGE_0_5_COL, AGE_5_17_COL, AGE_18_PLUS_COL]
    age_cols = [c for c in age_cols if c in df.columns]
    
    if not age_cols:
        return pd.Series()
    
    totals = df[age_cols].sum()
    percentages = (totals / totals.sum() * 100).round(2)
    
    return percentages

def temporal_trends(df):
    """Analyze enrollment trends over time."""
    if 'Year_Month' not in df.columns or 'Total_Enrollments' not in df.columns:
        return pd.DataFrame()
    
    monthly = df.groupby('Year_Month').agg({
        'Total_Enrollments': 'sum',
        STATE_COL: 'nunique'
    }).sort_index()
    
    monthly.columns = ['Total_Enrollments', 'States_Covered']
    
    return monthly

def detect_anomalies(df, column='Total_Enrollments', threshold=3):
    """Detect outliers using Z-score method."""
    if column not in df.columns:
        return pd.DataFrame()
    
    data = df[column].dropna()
    z_scores = np.abs(stats.zscore(data))
    
    anomalies = df[z_scores > threshold].copy()
    anomalies['Z_Score'] = z_scores[z_scores > threshold]
    
    return anomalies.sort_values('Z_Score', ascending=False)

def top_bottom_performers(df, metric='Total_Enrollments', n=10):
    """Identify top and bottom performing states/districts."""
    if STATE_COL not in df.columns or metric not in df.columns:
        return {}, {}
    
    state_totals = df.groupby(STATE_COL)[metric].sum().sort_values(ascending=False)
    
    top = state_totals.head(n)
    bottom = state_totals.tail(n)
    
    return top, bottom
