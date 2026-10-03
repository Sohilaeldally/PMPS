from pathlib import Path

import pandas as pd
from xgboost import Booster, DMatrix

from preprocessing import add_rolling_features, get_feature_columns
from config import ROLLING_SENSORS, ROLLING_WINDOWS


MODEL_PATH = Path("../models/final_xgboost_v3.json")


def load_model():
    model = Booster()
    model.load_model(MODEL_PATH)
    return model


def predict_rul(df: pd.DataFrame) -> float:
    df = df.copy()

    df = df.sort_values(
        ["unit_number", "time_cycles"]
    )

    df = add_rolling_features(
        df,
        sensors=ROLLING_SENSORS,
        windows=ROLLING_WINDOWS
    )

    model = load_model()

    feature_cols= get_feature_columns(df)
     

    latest_row = (
        df
        .sort_values(["unit_number", "time_cycles"])
        .tail(1)
    )

    prediction = model.predict(
        DMatrix(latest_row[feature_cols])
    )

    return float(prediction[0])