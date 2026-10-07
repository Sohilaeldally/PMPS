import pandas as pd
from xgboost import Booster, DMatrix

from preprocessing import add_rolling_features
from config import ROLLING_SENSORS, ROLLING_WINDOWS, MODEL_FEATURES, MODELS_DIR

MODEL_PATH = MODELS_DIR / "final_xgboost_v3.json"


def load_model():
    model = Booster()
    model.load_model(MODEL_PATH)
    return model


def predict_rul(df: pd.DataFrame, model) -> float:
    df = df.copy()

    df = df.sort_values(
        ["unit_number", "time_cycles"]
    )

    df = add_rolling_features(
        df,
        sensors=ROLLING_SENSORS,
        windows=ROLLING_WINDOWS
    )

    latest_row = df.tail(1)

    prediction = model.predict(
        DMatrix(latest_row[MODEL_FEATURES])
    )

    return float(prediction[0])


def predict_all_engines(df: pd.DataFrame) -> pd.DataFrame:
    model = load_model()

    predictions = []

    for engine_id in df["unit_number"].unique():
        engine_data = df[
            df["unit_number"] == engine_id
        ].copy()

        predicted_rul = predict_rul(engine_data, model)

        predictions.append({
            "unit_number": engine_id,
            "predicted_RUL": predicted_rul
        })

    return pd.DataFrame(predictions)