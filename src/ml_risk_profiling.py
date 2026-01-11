import pandas as pd


def build_state_risk_profile(forecast_df, anomaly_df):
    """
    Builds a state-level risk profile using:
    - Avg growth
    - Volatility
    - ML anomaly frequency
    """

    df = forecast_df.copy()

    # ----- Growth: average month-to-month percentage change -----
    df['Pct_Change'] = (
        df.groupby('State')['Total_Enrollments']
        .pct_change()
        .replace([float('inf'), float('-inf')], 0)
    )

    growth = (
        df.groupby('State')['Pct_Change']
        .mean()
        .fillna(0)
        .rename('Avg_Growth')
    )

    # ----- Volatility: standard deviation of enrollments -----
    volatility = (
        df.groupby('State')['Total_Enrollments']
        .std()
        .fillna(0)
        .rename('Volatility')
    )

    # ----- Anomaly count per state -----
    anomaly_count = (
        anomaly_df.groupby('State')
        .size()
        .rename('Anomalies')
        if not anomaly_df.empty
        else pd.Series(dtype=int, name='Anomalies')
    )

    # ----- Combine metrics -----
    risk_df = pd.concat(
        [growth, volatility, anomaly_count],
        axis=1
    ).fillna(0)

    # ----- Risk classification -----
    risk_df['Risk_Level'] = 'Low'

    risk_df.loc[
        (risk_df['Volatility'] > risk_df['Volatility'].quantile(0.75)) |
        (risk_df['Anomalies'] >= 2),
        'Risk_Level'
    ] = 'High'

    risk_df.loc[
    (risk_df['Risk_Level'] != 'High') &
    (risk_df['Volatility'] > risk_df['Volatility'].quantile(0.5)),
    'Risk_Level'
     ] = 'Medium'
 

    # ----- Explicit risk ordering -----
    risk_order = {'High': 0, 'Medium': 1, 'Low': 2}
    risk_df['Risk_Order'] = risk_df['Risk_Level'].map(risk_order)

    return (
        risk_df
        .reset_index()
        .sort_values(['Risk_Order', 'Volatility'], ascending=[True, False])
        .drop(columns=['Risk_Order'])
    )
