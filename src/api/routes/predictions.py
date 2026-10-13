from fastapi import APIRouter, HTTPException

from api.services import prediction_service

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.get("/latest")
def latest_predictions():
    return prediction_service.get_latest_predictions_with_status()


@router.get("/history/{engine_id}")
def prediction_history(engine_id: int):
    return prediction_service.get_prediction_history(engine_id)


@router.post("/{engine_id}")
def create_prediction(engine_id: int):
    result = prediction_service.create_prediction(engine_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"No sensor data found for engine {engine_id}",
        )

    return result