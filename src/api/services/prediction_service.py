from db.queries import (
    get_latest_predictions,
    get_engine_history,
    get_prediction_history as db_get_prediction_history,
    get_simulation_predictions,
)
from ml.predict import predict_engine_from_db
from api.services.alerts import get_maintenance_status


def get_latest_predictions_with_status():
    rows = get_latest_predictions()

    return [
        {
            "id": row[0],
            "engine_id": row[1],
            "predicted_rul": row[2],
            "prediction_time": row[3],
            "maintenance_status": get_maintenance_status(float(row[2])),
        }
        for row in rows
    ]


def get_prediction_history(engine_id: int):
    rows = db_get_prediction_history(engine_id)

    return [
        {
            "id": row[0],
            "engine_id": row[1],
            "predicted_rul": row[2],
            "prediction_time": row[3],
        }
        for row in rows
    ]


def create_prediction(engine_id: int):
    history = get_engine_history(engine_id)

    if history.empty:
        return None

    predicted_rul = predict_engine_from_db(engine_id)
    status = get_maintenance_status(predicted_rul)

    return {
        "engine_id": engine_id,
        "predicted_rul": predicted_rul,
        "maintenance_status": status,
    }


def get_simulation_results(simulation_id: str):
    return get_simulation_predictions(simulation_id)