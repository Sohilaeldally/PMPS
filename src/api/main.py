from fastapi import FastAPI, HTTPException

from db.queries import (
    get_latest_predictions,
    get_engine_history,
    get_prediction_history,
    get_simulation_predictions,
)

from ml.predict import predict_engine_from_db
from api.alerts import get_maintenance_status


app = FastAPI(
    title="PredMaint API",
    description="Predictive Maintenance Platform",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "PredMaint API is running!"
    }


@app.get("/predictions/latest")
def latest_predictions():
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


@app.get("/predictions/history/{engine_id}")
def prediction_history(engine_id: int):
    rows = get_prediction_history(engine_id)

    return [
        {
            "id": row[0],
            "engine_id": row[1],
            "predicted_rul": row[2],
            "prediction_time": row[3],
        }
        for row in rows
    ]


@app.post("/predictions/{engine_id}")
def create_prediction(engine_id: int):
    history = get_engine_history(engine_id)

    if history.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No sensor data found for engine {engine_id}",
        )

    predicted_rul = predict_engine_from_db(engine_id)
    status = get_maintenance_status(predicted_rul)

    return {
        "engine_id": engine_id,
        "predicted_rul": predicted_rul,
        "maintenance_status": status,
    }


@app.get("/simulations/{simulation_id}")
def simulation_predictions(simulation_id: str):
    try:
        rows = get_simulation_predictions(simulation_id)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="Could not retrieve simulation results. Check the simulation ID.",
        ) from exc

    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"No simulation results found for simulation ID {simulation_id}",
        )

    return rows
