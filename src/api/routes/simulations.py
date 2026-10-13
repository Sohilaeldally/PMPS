from fastapi import APIRouter, HTTPException

from api.services import prediction_service

router = APIRouter(prefix="/simulations", tags=["simulations"])


@router.get("/{simulation_id}")
def simulation_predictions(simulation_id: str):
    try:
        rows = prediction_service.get_simulation_results(simulation_id)
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