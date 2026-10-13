from fastapi import FastAPI

from api.routes import predictions, simulations

app = FastAPI(
    title="PredMaint API",
    description="Predictive Maintenance Platform",
    version="1.0.0"
)

app.include_router(predictions.router)
app.include_router(simulations.router)


@app.get("/")
def home():
    return {
        "message": "PredMaint API is running!"
    }