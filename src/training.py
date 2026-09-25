"""
Training utilities for the Predictive Maintenance project.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def split_by_engine(df: pd.DataFrame,test_size: float = 0.2,random_state: int = 42) -> tuple[pd.DataFrame, pd.DataFrame]:
    engine_ids = df["unit_number"].unique()

    train_engines, val_engines = train_test_split(
        engine_ids,
        test_size=test_size,
        random_state=random_state
    )

    train_data = df[df["unit_number"].isin(train_engines)].copy()

    val_data = df[df["unit_number"].isin(val_engines)].copy()

    return train_data, val_data


def evaluate_model(y_true: pd.Series, y_pred, model_name: str = "model") -> dict:
    """
    يحسب MAE, RMSE, R² لأي موديل، بدل ما تتكرر نفس الأسطر
    (mean_absolute_error / mean_squared_error / r2_score) في كل مرة.
    """
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    results = {
        "model": model_name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
    }

    print(model_name)
    print("MAE :", mae)
    print("RMSE:", rmse)
    print("R²  :", r2)

    return results


def build_error_analysis(val_data: pd.DataFrame, y_pred) -> pd.DataFrame:
    """
    يبني جدول تحليل الأخطاء (predicted_RUL, error, absolute_error)
    اللي كنا بنعمله يدويًا جوه النوتبوك.
    """
    error_analysis = val_data[["unit_number", "time_cycles", "RUL"]].copy()

    error_analysis["predicted_RUL"] = y_pred
    error_analysis["error"] = error_analysis["predicted_RUL"] - error_analysis["RUL"]
    error_analysis["absolute_error"] = error_analysis["error"].abs()

    return error_analysis