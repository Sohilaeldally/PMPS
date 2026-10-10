from fastapi import FastAPI

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
