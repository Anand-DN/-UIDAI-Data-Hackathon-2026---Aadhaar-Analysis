# UIDAI Data Hackathon 2026 - Aadhaar Analysis

**Unlocking Societal Trends in Aadhaar Enrolment and Updates**

## 📊 Project Overview

Comprehensive analysis of 1M+ Aadhaar enrollment records, 2M+ demographic updates, and 1.8M+ biometric updates to identify patterns, anomalies, and actionable insights for system improvements.

### Key Findings
- **2.6M enrollments** analyzed across 44 states and 938 districts
- **60% children (0-5 years)** dominate enrollments - strong birth integration
- **January 2025 spike**: 1.36M enrollments (6.3x above average) - successful campaign
- **Top 5 states** account for 54% of all enrollments - geographic concentration
- **60+ age anomalies** detected across states requiring policy attention
- **Data quality issues** identified: state name inconsistencies, >100% update rates

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

```bash
# Clone repository
git clone https://github.com/Anand-DN/-UIDAI-Data-Hackathon-2026---Aadhaar-Analysis.git
cd uidai-hackathon-2026

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


# Place UIDAI CSV files in respective folders:
# - data/enrolment/*.csv
# - data/demographic/*.csv
# - data/biometric/*.csv

# Run complete analysis
python main.py


📁 **Project Structure**
uidai-hackathon-2026/
├── data/
│   ├── enrolment/          # Enrollment CSV files
│   ├── demographic/        # Demographic update CSVs
│   └── biometric/          # Biometric update CSVs
├── src/
│   ├── config.py          # Configuration & paths
│   ├── loader.py          # Data loading utilities
│   ├── cleaning.py        # Data cleaning & standardization
│   ├── analysis.py        # Basic statistical analysis
│   ├── advanced_analysis.py   # Anomaly detection, compliance
│   ├── visuals.py         # Basic visualizations
│   ├── advanced_visuals.py    # Advanced charts
│   └── report.py          # PDF generation
├── outputs/
│   ├── figures/           # Generated visualizations
│   └── *.pdf             # Final report
├── main.py               # Main execution script
├── requirements.txt      # Python dependencies
└── README.md            # This file
