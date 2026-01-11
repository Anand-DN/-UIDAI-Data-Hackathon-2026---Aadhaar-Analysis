import pandas as pd
import numpy as np
from scipy import stats
from .config import (
    DIST_COL, DATE_COL,
    AGE_0_5_COL, AGE_5_17_COL, AGE_18_PLUS_COL
)


def _get_state_col(df):
    """Safely detect the state column regardless of casing."""
    for col in df.columns:
        if col.lower() == "state":
            return col
    return None


def get_summary_stats(enrol, demo, bio):
    """Generate basic summary statistics."""
    state_col = _get_state_col(enrol)

    summary = {
        'enrol_records': len(enrol),
        'demo_records': len(demo),
        'bio_records': len(bio),
        'date_range_enrol': (
            f"{enrol[DATE_COL].min()} to {enrol[DATE_COL].max()}"
            if DATE_COL in enrol else "N/A"
        ),
        'unique_states': enrol[state_col].nunique() if state_col else 0,
        'unique_districts': enrol[DIST_COL].nunique() if DIST_COL in enrol else 0,
    }

    if 'Total_Enrollments' in enrol.columns:
        summary['total_enrollments'] = int(enrol['Total_Enrollments'].sum())

    return summary


def state_wise_analysis(df):
    """Analyze enrollments by state."""
    state_col = _get_state_col(df)

    if not state_col or 'Total_Enrollments' not in df.columns:
        return pd.DataFrame()

    state_stats = (
        df
        .groupby(state_col)
        .agg(
            Total_Enrollments=('Total_Enrollments', 'sum'),
            Avg_per_Record=('Total_Enrollments', 'mean'),
            StdDev=('Total_Enrollments', 'std'),
            Record_Count=(DATE_COL, 'count')
        )
        .round(2)
        .sort_values('Total_Enrollments', ascending=False)
    )

    return state_stats


def age_group_distribution(df):
    """Calculate percentage distribution across age groups."""
    age_cols = [
        c for c in [AGE_0_5_COL, AGE_5_17_COL, AGE_18_PLUS_COL]
        if c in df.columns
    ]

    if not age_cols:
        return pd.Series(dtype=float)

    totals = df[age_cols].sum()
    percentages = (totals / totals.sum() * 100).round(2)

    return percentages


def temporal_trends(df):
    """Analyze enrollment trends over time."""
    state_col = _get_state_col(df)

    if 'Year_Month' not in df.columns or 'Total_Enrollments' not in df.columns:
        return pd.DataFrame()

    monthly = (
        df
        .groupby('Year_Month')
        .agg(
            Total_Enrollments=('Total_Enrollments', 'sum'),
            States_Covered=(state_col, 'nunique') if state_col else ('Total_Enrollments', 'size')
        )
        .reset_index()
    )

    return monthly


def detect_anomalies(df, column='Total_Enrollments', threshold=3):
    """Detect outliers using Z-score method."""
    if column not in df.columns:
        return pd.DataFrame()

    z_scores = np.abs(stats.zscore(df[column].fillna(0)))
    anomalies = df[z_scores > threshold].copy()
    anomalies['Z_Score'] = z_scores[z_scores > threshold]

    return anomalies.sort_values('Z_Score', ascending=False)


def top_bottom_performers(df, metric='Total_Enrollments', n=10):
    """Identify top and bottom performing states."""
    state_col = _get_state_col(df)

    if not state_col or metric not in df.columns:
        return {}, {}

    state_totals = (
        df
        .groupby(state_col)[metric]
        .sum()
        .sort_values(ascending=False)
    )

    return state_totals.head(n), state_totals.tail(n)
