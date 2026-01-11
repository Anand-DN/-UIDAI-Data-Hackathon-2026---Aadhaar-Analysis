from src.ml_visuals import (
    plot_actual_vs_predicted,
    plot_anomaly_timeline,
    plot_feature_importance
)

from src.loader import load_all
from src.cleaning import clean_dataset
from src.analysis import (
    get_summary_stats,
    state_wise_analysis,
    age_group_distribution,
    temporal_trends,
    detect_anomalies,
    top_bottom_performers
)
from src.visuals import (
    plot_age_distribution,
    plot_top_states,
    plot_monthly_trend,
    plot_state_age_heatmap
)
from src.report import generate_comprehensive_pdf

# ML imports
from src.ml_forecasting import train_forecast_model
from src.ml_anomaly import detect_ml_anomalies
from src.ml_risk_profiling import build_state_risk_profile


def normalize_state_column(df):
    """
    Detects the state column safely, standardizes names,
    and renames it to 'State' for downstream consistency.
    """
    state_col = None
    for col in df.columns:
        if col.lower() == "state":
            state_col = col
            break

    if state_col is None:
        raise ValueError(f"No state column found. Columns: {df.columns.tolist()}")

    df[state_col] = (
        df[state_col]
        .astype(str)
        .str.replace("&", "And", regex=False)
        .str.replace("  ", " ", regex=False)
        .str.strip()
        .str.title()
    )

    if state_col != "State":
        df.rename(columns={state_col: "State"}, inplace=True)

    return df


def main():
    print("\n" + "=" * 60)
    print(" UIDAI HACKATHON 2026 - AADHAAR DATA ANALYSIS")
    print("=" * 60)

    # ==================== STEP 1: LOAD DATA ====================
    enrol_raw, demo_raw, bio_raw = load_all()

    # ==================== STEP 2: CLEAN DATA ====================
    print("\n" + "=" * 60)
    print("CLEANING DATA")
    print("=" * 60)

    enrol = clean_dataset(enrol_raw, "Enrollment")
    demo = clean_dataset(demo_raw, "Demographic Updates")
    bio = clean_dataset(bio_raw, "Biometric Updates")

    # ==================== NORMALIZE STATE COLUMN (CRITICAL) ====================
    enrol = normalize_state_column(enrol)

    # ==================== STEP 3: SUMMARY ====================
    summary = get_summary_stats(enrol, demo, bio)

    # ==================== STEP 4–9: ANALYSIS & VISUALS ====================
    state_stats = state_wise_analysis(enrol)
    age_dist = age_group_distribution(enrol)
    monthly = temporal_trends(enrol)
    anomalies = detect_anomalies(enrol)
    top, bottom = top_bottom_performers(enrol)

    visualizations = {
        "Age Group Distribution": plot_age_distribution(enrol),
        "Top States by Enrollment": plot_top_states(enrol),
        "Monthly Enrollment Trend": plot_monthly_trend(enrol),
        "State vs Age Group Heatmap": plot_state_age_heatmap(enrol),
    }

    # ==================== STEP 10: INSIGHTS ====================
    insights = f"""
- Total enrollments analyzed: {summary.get('total_enrollments', 'N/A'):,}
- Geographic coverage: {summary['unique_states']} states, {summary['unique_districts']} districts
- Age distribution: {age_dist.to_dict() if not age_dist.empty else 'N/A'}
- {len(anomalies)} statistical anomalies detected
- Top performing state: {top.index[0] if not top.empty else 'N/A'}
""".strip()

    # ==================== STEP 11: MACHINE LEARNING ====================
    print("\n🤖 MACHINE LEARNING ANALYSIS")

    forecast_model, forecast_df, forecast_metrics = train_forecast_model(enrol)

    ml_anomalies, anomaly_model = detect_ml_anomalies(forecast_df)

    # --- Aggregate for national-level plots ---
    viz_df = (
        forecast_df
        .groupby('Year_Month', as_index=False)
        .agg({'Total_Enrollments': 'sum', 'Predicted': 'sum'})
    )

    viz_anomalies = (
        ml_anomalies
        .groupby('Year_Month', as_index=False)
        .agg({'Total_Enrollments': 'sum'})
    )

    # --- ML plots ---
    ml_forecast_plot = plot_actual_vs_predicted(viz_df)
    ml_anomaly_plot = plot_anomaly_timeline(viz_df, viz_anomalies)

    # --- Feature importance plot ---
    ml_feature_plot = plot_feature_importance(
        forecast_model,
        feature_names=[
            'State_Code', 'Year', 'Month', 'Quarter',
            'Lag_1', 'Lag_2', 'Lag_3', 'Rolling_3'
        ]
    )

    # --- ML summary ---
    ml_summary = {
        "forecast_mae": round(forecast_metrics["MAE"], 2),
        "anomaly_count": len(ml_anomalies),
        "states_covered": forecast_metrics["States_Covered"],
    }

    # ==================== STEP 12: STATE RISK PROFILING ====================
    state_risk_table = build_state_risk_profile(
        forecast_df=forecast_df,
        anomaly_df=ml_anomalies
    )

    # ==================== STEP 13: PDF REPORT ====================
    print("\n" + "=" * 60)
    print("GENERATING PDF REPORT")
    print("=" * 60)

    pdf_path = generate_comprehensive_pdf(
        summary=summary,
        visualizations=visualizations,
        insights=insights,
        ml_summary=ml_summary,
        ml_forecast_plot=ml_forecast_plot,
        ml_anomaly_plot=ml_anomaly_plot,
        ml_feature_plot=ml_feature_plot,
        state_risk_table=state_risk_table
    )

    print(f"\n✓ PDF Report saved to: {pdf_path}")
    print("\nANALYSIS COMPLETE!")


if __name__ == "__main__":
    main()
