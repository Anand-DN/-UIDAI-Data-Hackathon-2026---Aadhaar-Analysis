from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
FIG_DIR = OUTPUT_DIR / "figures"

for d in [OUTPUT_DIR, FIG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Your exact folder structure
ENROL_FILES = list((DATA_DIR / "enrolment").glob("*.csv"))
DEMO_FILES = list((DATA_DIR / "demographic").glob("*.csv"))
BIO_FILES = list((DATA_DIR / "biometric").glob("*.csv"))

# UIDAI column names (matching actual CSV headers - all lowercase)
DATE_COL = "date"
STATE_COL = "state"
DIST_COL = "district"
PIN_COL = "pincode"

# Age columns - UIDAI uses aggregated counts by age group
AGE_0_5_COL = "age_0_5"
AGE_5_17_COL = "age_5_17"
AGE_18_PLUS_COL = "age_18_greater"
