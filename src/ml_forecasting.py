import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error


def train_forecast_model(enrol_df):
    """
    FULL DATA ML FORECASTING
    - State-wise
    - Month-wise
    - Robust to column naming
    """

    # ==================== DETECT STATE COLUMN ====================
    possible_state_cols = [
        'State', 'state', 'State_Name', 'STATE',
        'Registrar_State', 'State/UT'
    ]

    state_col = None
    for col in possible_state_cols:
        if col in enrol_df.columns:
            state_col = col
            break

    if state_col is None:
        raise ValueError(
            f"No state column found. Available columns: {enrol_df.columns.tolist()}"
        )

    if 'Year_Month' not in enrol_df.columns:
        raise ValueError("Year_Month column missing in enrollment data.")

    # ==================== AGGREGATE TO STATE–MONTH ====================
    df = (
        enrol_df
        .groupby([state_col, 'Year_Month'])['Total_Enrollments']
        .sum()
        .reset_index()
        .rename(columns={state_col: 'State'})
        .sort_values(['State', 'Year_Month'])
    )

    # ==================== TEMPORAL FEATURES (✅ FIX HERE) ====================
    # Convert Year_Month string → datetime ONLY for ML
    df['Year_Month_DT'] = pd.to_datetime(df['Year_Month'], format='%Y-%m')

    df['Year'] = df['Year_Month_DT'].dt.year
    df['Month'] = df['Year_Month_DT'].dt.month
    df['Quarter'] = df['Year_Month_DT'].dt.quarter

    # ==================== LAG FEATURES (PER STATE) ====================
    for lag in [1, 2, 3]:
        df[f'Lag_{lag}'] = df.groupby('State')['Total_Enrollments'].shift(lag)

    df['Rolling_3'] = (
        df.groupby('State')['Total_Enrollments']
        .rolling(3)
        .mean()
        .reset_index(level=0, drop=True)
    )

    df.dropna(inplace=True)

    # ==================== ENCODE STATE ====================
    le = LabelEncoder()
    df['State_Code'] = le.fit_transform(df['State'])

    features = [
        'State_Code', 'Year', 'Month', 'Quarter',
        'Lag_1', 'Lag_2', 'Lag_3', 'Rolling_3'
    ]

    X = df[features]
    y = df['Total_Enrollments']

    # ==================== TRAIN MODEL ====================
    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X, y)

    # ==================== EVALUATION ====================
    preds = model.predict(X)
    mae = mean_absolute_error(y, preds)

    df['Predicted'] = preds

    metrics = {
        "MAE": mae,
        "Total_State_Months": len(df),
        "States_Covered": df['State'].nunique()
    }

    return model, df, metrics
