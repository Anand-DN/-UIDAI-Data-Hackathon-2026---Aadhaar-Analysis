from src.loader import load_all
from src.cleaning import clean_dataset
from src.analysis import (
    get_summary_stats, state_wise_analysis, age_group_distribution,
    temporal_trends, detect_anomalies, top_bottom_performers
)
from src.visuals import (
    plot_age_distribution, plot_top_states, 
    plot_monthly_trend, plot_state_age_heatmap
)
from src.report import generate_pdf_report

def main():
    print("\n" + "="*60)
    print(" UIDAI HACKATHON 2026 - AADHAAR DATA ANALYSIS")
    print("="*60)

    # STEP 1: Load data
    enrol_raw, demo_raw, bio_raw = load_all()

    # STEP 2: Clean data
    print("\n" + "="*60)
    print("CLEANING DATA")
    print("="*60)
    enrol = clean_dataset(enrol_raw, "Enrollment")
    demo = clean_dataset(demo_raw, "Demographic Updates")
    bio = clean_dataset(bio_raw, "Biometric Updates")

    # STEP 3: Summary statistics
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    summary = get_summary_stats(enrol, demo, bio)
    for key, value in summary.items():
        print(f"  {key}: {value}")

    # STEP 4: State-wise analysis
    print("\n" + "="*60)
    print("STATE-WISE ANALYSIS (Top 10)")
    print("="*60)
    state_stats = state_wise_analysis(enrol)
    print(state_stats.head(10))

    # STEP 5: Age distribution
    print("\n" + "="*60)
    print("AGE GROUP DISTRIBUTION")
    print("="*60)
    age_dist = age_group_distribution(enrol)
    print(age_dist)

    # STEP 6: Temporal trends
    print("\n" + "="*60)
    print("MONTHLY TRENDS (First 10 months)")
    print("="*60)
    monthly = temporal_trends(enrol)
    print(monthly.head(10))

    # STEP 7: Anomaly detection
    print("\n" + "="*60)
    print("ANOMALY DETECTION (Top 5 outliers)")
    print("="*60)
    anomalies = detect_anomalies(enrol)
    if not anomalies.empty:
        print(anomalies[['state', 'district', 'Total_Enrollments', 'Z_Score']].head())
    else:
        print("No anomalies detected")

    # STEP 8: Top/Bottom performers
    print("\n" + "="*60)
    print("TOP & BOTTOM PERFORMERS")
    print("="*60)
    top, bottom = top_bottom_performers(enrol)
    print("\nTop 5 States:")
    print(top.head())
    print("\nBottom 5 States:")
    print(bottom.head())

    # STEP 9: Generate visualizations
    print("\n" + "="*60)
    print("GENERATING VISUALIZATIONS")
    print("="*60)
    
    visualizations = {
        "Age Group Distribution": plot_age_distribution(enrol),
        "Top States by Enrollment": plot_top_states(enrol),
        "Monthly Enrollment Trend": plot_monthly_trend(enrol),
        "State vs Age Group Heatmap": plot_state_age_heatmap(enrol),
    }
    
    for name, path in visualizations.items():
        if path:
            print(f"  ✓ Created: {name}")

    # STEP 10: Generate insights text
    insights = f"""
- Total enrollments analyzed: {summary.get('total_enrollments', 'N/A'):,}
- Geographic coverage: {summary['unique_states']} states and {summary['unique_districts']} districts
- Age distribution: {age_dist.to_dict() if not age_dist.empty else 'N/A'}
- Peak enrollment periods identified in temporal analysis
- {len(anomalies)} anomalies detected requiring further investigation
- Top performing state: {top.index[0] if not top.empty else 'N/A'} with {int(top.iloc[0]):,} enrollments
- Significant variations observed across states suggesting policy intervention opportunities
    """.strip()

    # STEP 11: Generate PDF report
    print("\n" + "="*60)
    print("GENERATING PDF REPORT")
    print("="*60)
    
    pdf_path = generate_pdf_report(summary, visualizations, insights)
    print(f"\n✓ PDF Report saved to: {pdf_path}")

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60)
    print(f"\nOutputs saved in: outputs/")
    print(f"  - PDF Report: UIDAI_Hackathon_Analysis_Report.pdf")
    print(f"  - Figures: outputs/figures/")
    print("\n")

if __name__ == "__main__":
    main()
