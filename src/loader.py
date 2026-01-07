import pandas as pd
from .config import ENROL_FILES, DEMO_FILES, BIO_FILES

def load_concat(files):
    """Load and concatenate multiple CSV files."""
    if not files:
        return pd.DataFrame()
    
    dfs = []
    for f in files:
        print(f"Loading: {f.name}")
        df = pd.read_csv(f, low_memory=False)
        dfs.append(df)
    
    result = pd.concat(dfs, ignore_index=True)
    print(f"  → Total rows: {len(result):,}")
    return result

def load_all():
    """Load all three datasets."""
    print("\n" + "="*50)
    print("LOADING DATASETS")
    print("="*50)
    
    print("\n1. ENROLMENT DATA:")
    enrol = load_concat(ENROL_FILES)
    
    print("\n2. DEMOGRAPHIC UPDATE DATA:")
    demo = load_concat(DEMO_FILES)
    
    print("\n3. BIOMETRIC UPDATE DATA:")
    bio = load_concat(BIO_FILES)
    
    return enrol, demo, bio
