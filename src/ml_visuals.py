import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src.config import FIG_DIR


def plot_actual_vs_predicted(df):
    """
    PURE VISUALIZATION.
    Expects df to already contain:
    - Year_Month
    - Total_Enrollments
    - Predicted
    """

    x = df['Year_Month'].astype(str)

    plt.figure(figsize=(10, 5))
    plt.plot(x, df['Total_Enrollments'], label='Actual')
    plt.plot(x, df['Predicted'], label='Predicted')
    plt.xticks(rotation=45)
    plt.title("Actual vs Predicted Aadhaar Enrollments")
    plt.legend()
    plt.tight_layout()

    path = FIG_DIR / "ml_actual_vs_predicted.png"
    plt.savefig(path)
    plt.close()
    return path


def plot_anomaly_timeline(df, anomalies_df):
    """
    PURE VISUALIZATION.
    """

    x = df['Year_Month'].astype(str)

    plt.figure(figsize=(10, 5))
    plt.plot(x, df['Total_Enrollments'], label='Enrollments')

    if anomalies_df is not None and not anomalies_df.empty:
        plt.scatter(
            anomalies_df['Year_Month'].astype(str),
            anomalies_df['Total_Enrollments'],
            color='red',
            label='Anomaly'
        )

    plt.xticks(rotation=45)
    plt.title("Enrollment Timeline with ML Anomalies")
    plt.legend()
    plt.tight_layout()

    path = FIG_DIR / "ml_anomaly_timeline.png"
    plt.savefig(path)
    plt.close()
    return path
import matplotlib.pyplot as plt
from .config import FIG_DIR


def plot_feature_importance(model, feature_names):
    """
    Plots Random Forest feature importance and saves the figure.
    Returns path to saved image.
    """

    importances = model.feature_importances_

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(feature_names, importances)
    ax.set_title("Feature Importance (Random Forest)")
    ax.set_xlabel("Importance Score")
    ax.set_ylabel("Feature")

    plt.tight_layout()

    output_path = FIG_DIR / "ml_feature_importance.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    return output_path
