import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from .config import FIG_DIR, STATE_COL, AGE_0_5_COL, AGE_5_17_COL, AGE_18_PLUS_COL

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10

def plot_age_distribution(df):
    """Plot age group distribution pie chart."""
    age_cols = [AGE_0_5_COL, AGE_5_17_COL, AGE_18_PLUS_COL]
    age_cols = [c for c in age_cols if c in df.columns]
    
    if not age_cols:
        return None
    
    totals = df[age_cols].sum()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    wedges, texts, autotexts = ax.pie(
        totals, 
        labels=['0-5 years', '5-17 years', '18+ years'][:len(totals)],
        autopct='%1.1f%%',
        colors=colors,
        startangle=90
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
        autotext.set_weight('bold')
    
    ax.set_title('Enrollment Distribution by Age Group', fontsize=14, weight='bold')
    
    path = FIG_DIR / "age_distribution.png"
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return path

def plot_top_states(df, top_n=15):
    """Plot top N states by enrollment."""
    if STATE_COL not in df or 'Total_Enrollments' not in df:
        return None
    
    state_totals = df.groupby(STATE_COL)['Total_Enrollments'].sum().sort_values(ascending=False).head(top_n)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(range(len(state_totals)), state_totals.values, color='steelblue')
    ax.set_yticks(range(len(state_totals)))
    ax.set_yticklabels(state_totals.index)
    ax.set_xlabel('Total Enrollments', fontsize=11)
    ax.set_title(f'Top {top_n} States by Enrollment', fontsize=14, weight='bold')
    ax.invert_yaxis()
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, 
                f'{int(width):,}', 
                ha='left', va='center', fontsize=9)
    
    path = FIG_DIR / "top_states.png"
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return path

def plot_monthly_trend(df):
    """Plot enrollment trend over time."""
    if 'Year_Month' not in df or 'Total_Enrollments' not in df:
        return None
    
    monthly = df.groupby('Year_Month')['Total_Enrollments'].sum()
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(range(len(monthly)), monthly.values, marker='o', linewidth=2, markersize=4)
    ax.set_xticks(range(0, len(monthly), max(1, len(monthly)//12)))
    ax.set_xticklabels([str(monthly.index[i]) for i in range(0, len(monthly), max(1, len(monthly)//12))], rotation=45)
    ax.set_xlabel('Month', fontsize=11)
    ax.set_ylabel('Total Enrollments', fontsize=11)
    ax.set_title('Monthly Enrollment Trend', fontsize=14, weight='bold')
    ax.grid(True, alpha=0.3)
    
    path = FIG_DIR / "monthly_trend.png"
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return path

def plot_state_age_heatmap(df, top_n=20):
    """Create heatmap of state vs age group."""
    if STATE_COL not in df:
        return None
    
    age_cols = [AGE_0_5_COL, AGE_5_17_COL, AGE_18_PLUS_COL]
    age_cols = [c for c in age_cols if c in df.columns]
    
    if not age_cols:
        return None
    
    # Get top N states
    top_states = df.groupby(STATE_COL)['Total_Enrollments'].sum().nlargest(top_n).index
    
    # Create pivot
    pivot_data = df[df[STATE_COL].isin(top_states)].groupby(STATE_COL)[age_cols].sum()
    pivot_data.columns = ['0-5 yrs', '5-17 yrs', '18+ yrs'][:len(age_cols)]
    
    fig, ax = plt.subplots(figsize=(8, 10))
    sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Enrollments'})
    ax.set_title(f'State vs Age Group Heatmap (Top {top_n} States)', fontsize=14, weight='bold')
    ax.set_xlabel('Age Group', fontsize=11)
    ax.set_ylabel('State', fontsize=11)
    
    path = FIG_DIR / "state_age_heatmap.png"
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return path