from fastapi import FastAPI, HTTPException
from db.queries import get_latest_predictions, get_engine_history
from predict import predict_engine_from_db

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

    return {
        "engine_id": engine_id,
        "predicted_rul": predicted_rul,
    }