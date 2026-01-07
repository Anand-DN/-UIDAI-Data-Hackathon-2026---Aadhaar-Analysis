from src.loader import load_all
from src.cleaning import clean_dataset
from src.analysis import (
    get_summary_stats, state_wise_analysis, age_group_distribution,
    temporal_trends, detect_anomalies, top_bottom_performers
)
from src.advanced_analysis import (
    geographic_disparity_analysis, age_group_anomalies, temporal_anomaly_detection,
    merge_with_updates, update_compliance_analysis, 
    generate_insights, generate_recommendations
)
from src.visuals import (
    plot_age_distribution, plot_top_states, 
    plot_monthly_trend, plot_state_age_heatmap
)
from src.advanced_visuals import (
    plot_geographic_disparity, plot_age_anomalies, plot_temporal_anomalies,
    plot_update_compliance, plot_yoy_comparison, plot_correlation_heatmap
)
from src.report import generate_comprehensive_pdf

def main():
    print("\n" + "="*70)
    print(" UIDAI HACKATHON 2026 - COMPREHENSIVE AADHAAR ANALYSIS")
    print("="*70)

    # ==================== STEP 1: LOAD DATA ====================
    enrol_raw, demo_raw, bio_raw = load_all()

    # ==================== STEP 2: CLEAN DATA ====================
    print("\n" + "="*70)
    print("CLEANING DATA")
    print("="*70)
    enrol = clean_dataset(enrol_raw, "Enrollment")
    demo = clean_dataset(demo_raw, "Demographic Updates")
    bio = clean_dataset(bio_raw, "Biometric Updates")

    # ==================== STEP 3: BASIC ANALYSIS ====================
    print("\n" + "="*70)
    print("BASIC ANALYSIS")
    print("="*70)
    
    summary = get_summary_stats(enrol, demo, bio)
    print("\n📊 Summary Statistics:")
    for key, value in summary.items():
        print(f"   {key}: {value}")

    state_stats = state_wise_analysis(enrol)
    print(f"\n🏆 Top 10 States by Total Enrollments:")
    print(state_stats.head(10))

    age_dist = age_group_distribution(enrol)
    print(f"\n👶 Age Group Distribution (%):")
    print(age_dist)

    # ==================== STEP 4: ADVANCED ANALYSIS ====================
    print("\n" + "="*70)
    print("ADVANCED ANALYSIS")
    print("="*70)

    # Geographic disparity
    print("\n🗺️ Geographic Disparity Analysis...")
    state_efficiency, underperformers = geographic_disparity_analysis(enrol)
    print(f"\n⚠️ States needing intervention ({len(underperformers)}):")
    print(underperformers.head(10))

    # Age anomalies
    print("\n🔍 Detecting Age Distribution Anomalies...")
    age_anomalies, national_avg, state_age_pct = age_group_anomalies(enrol)
    print(f"\n⚡ Critical anomalies found: {len(age_anomalies)}")
    if not age_anomalies.empty:
        print(age_anomalies.head(10))

    # Temporal anomalies
    print("\n📈 Temporal Anomaly Detection...")
    temporal_anom, mom_growth, monthly = temporal_anomaly_detection(enrol)
    print(f"\n🚨 Unusual enrollment months:")
    print(temporal_anom.head())

    # Merge with updates
    print("\n🔗 Merging with Update Data...")
    merged = merge_with_updates(enrol, demo, bio)
    print(f"   Merged records: {len(merged):,}")

    # Update compliance
    print("\n📋 Update Compliance Analysis...")
    state_compliance, top_compliance, bottom_compliance = update_compliance_analysis(merged)
    if not state_compliance.empty:
        print("\n✅ Top 5 states by demographic update compliance:")
        print(top_compliance.head())
        print("\n❌ Bottom 5 states (need attention):")
        print(bottom_compliance.head())

    # ==================== STEP 5: GENERATE INSIGHTS ====================
    print("\n" + "="*70)
    print("GENERATING INSIGHTS")
    print("="*70)
    
    insights = generate_insights(
        enrol, demo, bio, state_stats, 
        temporal_anom, age_anomalies, state_compliance
    )
    
    print("\n💡 KEY INSIGHTS:")
    for i, insight in enumerate(insights, 1):
        print(f"   {i}. {insight}")

    # ==================== STEP 6: GENERATE RECOMMENDATIONS ====================
    print("\n" + "="*70)
    print("GENERATING RECOMMENDATIONS")
    print("="*70)
    
    recommendations = generate_recommendations(
        underperformers, age_anomalies, state_compliance
    )
    
    print(f"\n🎯 {len(recommendations)} ACTIONABLE RECOMMENDATIONS:")
    for idx, row in recommendations.iterrows():
        print(f"\n   {idx+1}. {row['Category']}")
        print(f"      Issue: {row['Issue']}")
        print(f"      Action: {row['Recommendation']}")

    # ==================== STEP 7: GENERATE VISUALIZATIONS ====================
    print("\n" + "="*70)
    print("GENERATING VISUALIZATIONS")
    print("="*70)
    
    visualizations = {
        # Basic
        "Age Group Distribution": plot_age_distribution(enrol),
        "Top States by Enrollment": plot_top_states(enrol),
        "Monthly Enrollment Trend": plot_monthly_trend(enrol),
        "State vs Age Group Heatmap": plot_state_age_heatmap(enrol),
        
        # Advanced
        "Geographic Disparity Analysis": plot_geographic_disparity(state_efficiency, underperformers),
        "Age Distribution Anomalies": plot_age_anomalies(age_anomalies, national_avg),
        "Temporal Anomalies": plot_temporal_anomalies(temporal_anom, monthly),
        "Update Compliance": plot_update_compliance(state_compliance),
        "Year-over-Year Comparison": plot_yoy_comparison(enrol),
        "Correlation Heatmap": plot_correlation_heatmap(enrol),
    }
    
    for name, path in visualizations.items():
        if path:
            print(f"   ✓ {name}")

    # ==================== STEP 8: GENERATE COMPREHENSIVE PDF ====================
    print("\n" + "="*70)
    print("GENERATING COMPREHENSIVE PDF REPORT")
    print("="*70)
    
    pdf_path = generate_comprehensive_pdf(
        summary, visualizations, insights, 
        recommendations, age_anomalies
    )
    
    print(f"\n✅ PDF Report Generated: {pdf_path}")

    # ==================== COMPLETION ====================
    print("\n" + "="*70)
    print("🎉 ANALYSIS COMPLETE!")
    print("="*70)

if __name__ == "__main__":
    main()
