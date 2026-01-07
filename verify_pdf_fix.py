from src.report import AdvancedHackathonReport
from fpdf import FPDF
import os

try:
    print("Testing PDF Generation with fixed text...")
    pdf = AdvancedHackathonReport()
    pdf.add_page()
    pdf.section_title("3.2 Analysis Techniques", level=2)
    # This is the exact list that was failing
    pdf.bullet_points([
        "Univariate Analysis: Distribution analysis, central tendency, dispersion",
        "Bivariate Analysis: State vs age group, temporal correlations",
        "Multivariate Analysis: Heatmaps, clustering, correlation matrices",
        "Anomaly Detection: Z-score method (threshold=2 sigma) for temporal and geographic outliers",
        "Compliance Analysis: Enrollment-to-update linkage and rate calculation",
        "Statistical Testing: Chi-square for categorical associations"
    ])
    output_path = "test_output.pdf"
    pdf.output(output_path)
    print("PDF generated successfully!")
    if os.path.exists(output_path):
        os.remove(output_path)
        print("Test output cleaned up.")
except Exception as e:
    print(f"FAILED: {e}")
