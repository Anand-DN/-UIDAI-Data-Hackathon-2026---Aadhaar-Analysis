from fpdf import FPDF
from datetime import datetime
from .config import OUTPUT_DIR


def safe_text(text):
    """
    Converts unicode characters to Latin-1 safe equivalents for FPDF.
    """
    if not isinstance(text, str):
        return text

    replacements = {
        "–": "-",
        "—": "-",
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "•": "-",
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text


class AdvancedHackathonReport(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 10, "UIDAI Data Hackathon 2026", ln=1, align="C")
        self.set_font("Helvetica", "B", 14)
        self.cell(
            0,
            7,
            "Unlocking Societal Trends in Aadhaar Enrolment and Updates",
            ln=1,
            align="C",
        )
        self.set_font("Helvetica", "I", 10)
        self.cell(
            0,
            5,
            f"Analysis Report | Generated: {datetime.now().strftime('%B %d, %Y')}",
            ln=1,
            align="C",
        )
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def section_title(self, title, level=1):
        if level == 1:
            self.set_font("Helvetica", "B", 14)
            self.set_fill_color(220, 230, 250)
        else:
            self.set_font("Helvetica", "B", 12)
            self.set_fill_color(240, 245, 255)

        self.cell(0, 10, title, ln=1, fill=True)
        self.ln(2)

    def section_body(self, text):
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5, safe_text(text))
        self.ln(3)

    def bullet_points(self, points):
        self.set_font("Helvetica", "", 10)
        indent = 10
        for point in points:
            self.set_x(self.l_margin + indent)
            effective_width = self.w - self.r_margin - (self.l_margin + indent)
            self.multi_cell(effective_width, 5, safe_text(f"- {point}"))
        self.ln(2)


def generate_comprehensive_pdf(
    summary,
    visualizations,
    insights,
    recommendations=None,
    age_anomalies_df=None,
    ml_summary=None,
    ml_forecast_plot=None,
    ml_anomaly_plot=None,
    ml_feature_plot=None,
    forecast_table=None,
    anomaly_table=None,
    state_risk_table=None,
):

    pdf = AdvancedHackathonReport()

    # ==================== 1. PROBLEM ====================
    pdf.add_page()
    pdf.section_title("1. Problem Statement & Approach")
    pdf.section_body(
        "This analysis examines anonymized Aadhaar enrollment, demographic update, "
        "and biometric update datasets published by UIDAI to identify patterns, trends, "
        "anomalies, and predictive indicators. The objective is to uncover meaningful "
        "temporal, geographic, and demographic patterns, identify operational anomalies, "
        "and develop predictive insights that can support data-driven policy planning "
        "and capacity optimization."
    )

    # ==================== 2. DATASETS ====================
    pdf.add_page()
    pdf.section_title("2. Datasets Used")

    pdf.section_title("2.1 Enrollment Dataset", level=2)
    pdf.section_body(
        f"Records analyzed: {summary['enrol_records']:,}\n"
        f"Date range: {summary['date_range_enrol']}\n"
        f"Geographic coverage: {summary['unique_states']} states, "
        f"{summary['unique_districts']} districts\n"
        f"Total enrollments: {summary.get('total_enrollments', 'N/A'):,}"
    )

    pdf.section_title("2.2 Demographic Update Dataset", level=2)
    pdf.section_body(f"Records analyzed: {summary['demo_records']:,}")

    pdf.section_title("2.3 Biometric Update Dataset", level=2)
    pdf.section_body(f"Records analyzed: {summary['bio_records']:,}")

    # ==================== 3. METHODOLOGY ====================
    pdf.add_page()
    pdf.section_title("3. Methodology")
    pdf.bullet_points(
        [
            "Data cleaning and validation",
            "Exploratory data analysis",
            "Statistical anomaly detection",
            "Machine learning based forecasting and anomaly detection",
            "All machine learning models were trained on the full aggregated dataset",
        ]
    )

    # ==================== 4. VISUAL ANALYSIS ====================
    viz_titles = {
        "Age Group Distribution": "4.1 Overall Age Distribution",
        "Top States by Enrollment": "4.2 Geographic Concentration",
        "Monthly Enrollment Trend": "4.3 Temporal Trends",
        "State vs Age Group Heatmap": "4.4 State-Age Group Patterns",
    }

    for title, section in viz_titles.items():
        if title in visualizations and visualizations[title] and visualizations[title].exists():
            pdf.add_page()
            pdf.section_title(section)
            pdf.image(str(visualizations[title]), x=15, w=180)

    # ==================== 5. INSIGHTS ====================
    pdf.add_page()
    pdf.section_title("5. Key Findings & Insights")

    if isinstance(insights, str):
        insights = [i.strip("- ").strip() for i in insights.split("\n") if i.strip()]
    pdf.bullet_points(insights)

    # ==================== 6. MACHINE LEARNING ====================
    pdf.add_page()
    pdf.section_title("6. Machine Learning Analysis")

    if ml_summary:
        pdf.section_title("6.1 Enrollment Forecasting", level=2)
        pdf.section_body(
            f"Random Forest model trained on full state-month data.\n\n"
            f"Mean Absolute Error (MAE): {ml_summary.get('forecast_mae', 'N/A')}\n"
            f"States covered: {ml_summary.get('states_covered', 'N/A')}"
        )

        if ml_forecast_plot:
            pdf.image(str(ml_forecast_plot), x=15, w=180)

        pdf.section_title("6.2 ML-based Anomaly Detection", level=2)
        pdf.section_body(
            f"Isolation Forest detected "
            f"{ml_summary.get('anomaly_count', 'N/A')} anomalous state-month periods."
        )

        if ml_anomaly_plot:
            pdf.image(str(ml_anomaly_plot), x=15, w=180)

        if ml_feature_plot:
            pdf.section_title("6.3 Feature Importance", level=2)
            pdf.section_body(
                "Feature importance analysis indicates that lag-based and rolling historical "
                "features are the strongest predictors, highlighting strong temporal dependence."
            )
            pdf.image(str(ml_feature_plot), x=25, w=160)

        pdf.section_title("6.4 Policy Relevance", level=2)
        pdf.section_body(
            "Machine learning enables predictive capacity planning and proactive monitoring "
            "of Aadhaar enrollment operations at a national scale."
        )

    # ==================== 7. STATE RISK PROFILING ====================
    if state_risk_table is not None and not state_risk_table.empty:
        pdf.add_page()
        pdf.section_title("7. State Risk Profiling")
        pdf.section_body(
            "States were classified into High, Medium, and Low risk categories based on "
            "enrollment volatility, growth instability, and machine learning detected anomalies."
            "Only High and Medium risk states are shown to highlight regions requiring "
            "immediate attention or closer monitoring. Low risk states are excluded for clarity."
             )

        
        pdf.ln(3)

        # Table header
        pdf.set_font("Helvetica", "B", 9)
        col_widths = [40, 22, 28, 28, 22]
        headers = ["State", "Risk", "Avg Growth", "Volatility", "Anomalies"]

        for h, w in zip(headers, col_widths):
            pdf.cell(w, 8, h, border=1)
        pdf.ln()

        # Table rows
        pdf.set_font("Helvetica", "", 9)
        filtered_risk = state_risk_table[
        state_risk_table['Risk_Level'].isin(['High', 'Medium'])
         ]

        for _, row in filtered_risk.iterrows():

            pdf.cell(col_widths[0], 7, safe_text(str(row["State"])), border=1)
            pdf.cell(col_widths[1], 7, safe_text(str(row["Risk_Level"])), border=1)
            pdf.cell(col_widths[2], 7, f"{row['Avg_Growth']*100:.2f}%", border=1)
            pdf.cell(col_widths[3], 7, f"{row['Volatility']:.0f}", border=1)
            pdf.cell(col_widths[4], 7, str(int(row["Anomalies"])), border=1)
            pdf.ln()

    # ==================== 8. CONCLUSION ====================
    pdf.add_page()
    pdf.section_title("8. Conclusion")
    pdf.section_body(
        "This study demonstrates how statistical analysis and machine learning together "
        "can support data-driven decision making for UIDAI."
    )

    output_path = OUTPUT_DIR / "UIDAI_Hackathon_Comprehensive_Analysis.pdf"
    pdf.output(str(output_path))

    return output_path
