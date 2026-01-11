import pandas as pd
import numpy as np
from .config import (
    DATE_COL, STATE_COL, DIST_COL, PIN_COL,
    AGE_0_5_COL, AGE_5_17_COL, AGE_18_PLUS_COL
)

def clean_dataset(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    """Clean any UIDAI dataset."""
    print(f"\nCleaning {dataset_name}...")
    original_rows = len(df)

    # 1. Standardize state names FIRST
    df = standardize_state_names(df)
    
    # 2. Convert date column
    if DATE_COL in df.columns:
        df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors='coerce')
        df = df.dropna(subset=[DATE_COL])  # Remove invalid dates
    
    # 3. Clean text columns
    text_cols = [STATE_COL, DIST_COL]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
    
    # 4. Clean numeric columns (PIN and age groups)
    if PIN_COL in df.columns:
        df[PIN_COL] = pd.to_numeric(df[PIN_COL], errors='coerce')
    
    for age_col in [AGE_0_5_COL, AGE_5_17_COL, AGE_18_PLUS_COL]:
        if age_col in df.columns:
            df[age_col] = pd.to_numeric(df[age_col], errors='coerce').fillna(0)
    
    # 5. Create total enrollment column
    age_cols = [c for c in [AGE_0_5_COL, AGE_5_17_COL, AGE_18_PLUS_COL] if c in df.columns]
    if age_cols:
        df['Total_Enrollments'] = df[age_cols].sum(axis=1)
    
    # 6. Extract temporal features  ✅ FIX HERE
    if DATE_COL in df.columns:
        df['Year'] = df[DATE_COL].dt.year
        df['Month'] = df[DATE_COL].dt.month
        df['Quarter'] = df[DATE_COL].dt.quarter
        df['Year_Month'] = df[DATE_COL].dt.to_period('M').astype(str)
    
    # 7. Remove duplicates
    df = df.drop_duplicates()
    
    print(f"  ✓ Cleaned: {original_rows:,} → {len(df):,} rows ({original_rows - len(df):,} removed)")
    
    return df


def standardize_state_names(df):
    """Fix inconsistent state names and remove invalid entries."""
    from .config import STATE_COL
    
    if STATE_COL not in df.columns:
        return df
    
    state_mapping = {
        'West Bangal': 'West Bengal',
        'Westbengal': 'West Bengal',
        'West  Bengal': 'West Bengal',
        'Daman And Diu': 'Daman & Diu',
        'Dadra And Nagar Haveli And Daman And Diu': 'Dadra & Nagar Haveli',
        'The Dadra And Nagar Haveli And Daman And Diu': 'Dadra & Nagar Haveli',
        'Andaman And Nicobar Islands': 'Andaman & Nicobar Islands',
        'Andaman & Nicobar': 'Andaman & Nicobar Islands',
        'Orissa': 'Odisha',
        '100000': 'INVALID',
        '10000': 'INVALID',
    }
    
    df[STATE_COL] = df[STATE_COL].replace(state_mapping)
    df = df[df[STATE_COL] != 'INVALID']
    df = df[~df[STATE_COL].str.match(r'^\d+$', na=False)]
    
    print("   State names standardized")
    
    return df
