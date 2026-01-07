import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from .config import FIG_DIR, STATE_COL

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300

def plot_geographic_disparity(state_stats, underperformers):
    """Plot enrollment efficiency by state."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Top 15 states by efficiency
    top_15 = state_stats.nlargest(15, 'Enrollments_Per_District')
    ax1.barh(range(len(top_15)), top_15['Enrollments_Per_District'].values, color='green', alpha=0.7)
    ax1.set_yticks(range(len(top_15)))
    ax1.set_yticklabels(top_15.index)
    ax1.set_xlabel('Enrollments Per District', fontsize=11)
    ax1.set_title('Top 15 Most Efficient States', fontsize=12, weight='bold')
    ax1.invert_yaxis()
    
    # Bottom 15 states (need attention)
    bottom_15 = state_stats.nsmallest(15, 'Enrollments_Per_District')
    ax2.barh(range(len(bottom_15)), bottom_15['Enrollments_Per_District'].values, color='red', alpha=0.7)
    ax2.set_yticks(range(len(bottom_15)))
    ax2.set_yticklabels(bottom_15.index)
    ax2.set_xlabel('Enrollments Per District', fontsize=11)
    ax2.set_title('Bottom 15 States (Need Intervention)', fontsize=12, weight='bold')
    ax2.invert_yaxis()
    
    plt.tight_layout()
    path = FIG_DIR / "geographic_disparity.png"
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    return path

def plot_age_anomalies(age_anomalies, national_avg):
    """Visualize age distribution anomalies."""
    if age_anomalies.empty:
        return None
    
    # Get top 10 states with largest deviations
    top_anomalies = age_anomalies.nlargest(10, 'Deviation')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(top_anomalies))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, top_anomalies['State_Pct'], width, 
                   label='State %', color='coral')
    bars2 = ax.bar(x + width/2, top_anomalies['National_Avg'], width,
                   label='National Avg %', color='skyblue')
    
    ax.set_xlabel('State - Age Group', fontsize=11)
    ax.set_ylabel('Percentage (%)', fontsize=11)
    ax.set_title('Top 10 Age Distribution Anomalies', fontsize=14, weight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f"{row['State']}\n({row['Age_Group']})" 
                        for _, row in top_anomalies.iterrows()], rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    path = FIG_DIR / "age_anomalies.png"
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    return path

def plot_temporal_anomalies(anomalies, monthly_trend):
    """Highlight temporal anomalies in enrollment trend."""
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot normal trend
    ax.plot(range(len(monthly_trend)), monthly_trend.values, 
            marker='o', linewidth=2, markersize=5, color='steelblue', label='Monthly Enrollments')
    
    # Highlight anomalies
    for month in anomalies.index:
        idx = monthly_trend.index.get_loc(month)
        ax.scatter(idx, anomalies[month], color='red', s=200, zorder=5, 
                   marker='*', label='Anomaly' if month == anomalies.index[0] else '')
    
    ax.set_xticks(range(0, len(monthly_trend), max(1, len(monthly_trend)//12)))
    ax.set_xticklabels([str(monthly_trend.index[i]) 
                        for i in range(0, len(monthly_trend), max(1, len(monthly_trend)//12))], 
                       rotation=45)
    ax.set_xlabel('Month', fontsize=11)
    ax.set_ylabel('Total Enrollments', fontsize=11)
    ax.set_title('Monthly Enrollment Trend with Anomalies Highlighted', fontsize=14, weight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    path = FIG_DIR / "temporal_anomalies.png"
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    return path

def plot_update_compliance(state_compliance):
    """Compare demographic vs biometric update rates."""
    if 'Demo_Update_Rate' not in state_compliance.columns:
        return None
    
    top_15 = state_compliance.nlargest(15, 'Total_Enrollments')
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    x = np.arange(len(top_15))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, top_15['Demo_Update_Rate'], width,
                   label='Demographic Update %', color='#66b3ff')
    bars2 = ax.bar(x + width/2, top_15['Bio_Update_Rate'], width,
                   label='Biometric Update %', color='#99ff99')
    
    ax.set_xlabel('State', fontsize=11)
    ax.set_ylabel('Update Rate (%)', fontsize=11)
    ax.set_title('Update Compliance: Top 15 States', fontsize=14, weight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(top_15.index, rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    path = FIG_DIR / "update_compliance.png"
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    return path

def plot_yoy_comparison(enrol):
    """Year-over-year enrollment comparison."""
    if 'Year' not in enrol.columns or 'Month' not in enrol.columns:
        return None
    
    yearly_monthly = enrol.groupby(['Year', 'Month'])['Total_Enrollments'].sum().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    for year in yearly_monthly.index:
        ax.plot(yearly_monthly.columns, yearly_monthly.loc[year], 
               marker='o', linewidth=2, label=f'Year {int(year)}')
    
    ax.set_xlabel('Month', fontsize=11)
    ax.set_ylabel('Total Enrollments', fontsize=11)
    ax.set_title('Year-over-Year Enrollment Comparison', fontsize=14, weight='bold')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    path = FIG_DIR / "yoy_comparison.png"
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    return path

def plot_correlation_heatmap(enrol):
    """Correlation heatmap of numeric features."""
    numeric_cols = enrol.select_dtypes(include=[np.number]).columns.tolist()
    
    # Remove redundant columns
    exclude = ['Year_Month']
    numeric_cols = [c for c in numeric_cols if c not in exclude]
    
    if len(numeric_cols) < 3:
        return None
    
    corr = enrol[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title('Feature Correlation Matrix', fontsize=14, weight='bold')
    
    plt.tight_layout()
    path = FIG_DIR / "correlation_heatmap.png"
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    return path
