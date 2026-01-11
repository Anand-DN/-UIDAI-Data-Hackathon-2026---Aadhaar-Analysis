import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder


def detect_ml_anomalies(state_month_df):
    """
    FULL DATA ANOMALY DETECTION
    - State × Month level
    - Entire dataset scanned
    """

    df = state_month_df.copy()

    # Encode state
    le = LabelEncoder()
    df['State_Code'] = le.fit_transform(df['State'])

    X = df[['State_Code', 'Year', 'Month', 'Total_Enrollments']]

    model = IsolationForest(
        contamination=0.03,
        random_state=42
    )

    df['Anomaly_Flag'] = model.fit_predict(X)
    df['Is_Anomaly'] = df['Anomaly_Flag'] == -1

    anomalies = df[df['Is_Anomaly']]

    return anomalies, model
