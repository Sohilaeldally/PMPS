# PMPS — Predictive Maintenance Platform System

Predictive maintenance pipeline for turbofan jet engines, built on NASA's
C-MAPSS (FD001) dataset. Predicts Remaining Useful Life (RUL) from sensor
readings and serves predictions through a REST API with maintenance alerts.

## Pipeline

Sensor Data → Cleaning / Feature Engineering → XGBoost Model → RUL Prediction
→ PostgreSQL → FastAPI → Maintenance Alerts


## Dataset

[NASA C-MAPSS (FD001)](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/) —
100 training engines and 100 test engines, 1 operating condition, 1 fault
mode (HPC degradation), 21 sensor channels per cycle.

## Project structure

```
PMPS/
├── data/                   # raw C-MAPSS files (not tracked in git)
├── models/                 # trained model artifacts (not tracked in git)
├── database/
│   └── schema.sql          # PostgreSQL table definitions
├── notebooks/
│   ├── 01_train_eda.ipynb
│   ├── 02_test_analysis.ipynb
│   ├── 03_baseline_modeling.ipynb
│   ├── 04_xgboost_tuning.ipynb
│   └── 05_test_evaluation.ipynb
├── src/
│   ├── config.py           # paths, DB config, model feature list
│   ├── ml/                 # preprocessing, training, prediction
│   ├── db/                 # PostgreSQL read/write queries
│   ├── api/                # FastAPI app and alert logic
│   └── test/               # simulation / smoke-test scripts
├── docker-compose.yml       # PostgreSQL service
└── requirements.txt
```


## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/Sohilaeldally/PMPS.git
cd PMPS
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Get the data

Download the C-MAPSS FD001 files (`train_FD001.txt`, `test_FD001.txt`,
`RUL_FD001.txt`) and place them in `data/`.

### 3. Start the database

```bash
cp .env.example .env    # fill in POSTGRES_PASSWORD
docker-compose up -d
```

Create the tables:
```bash
docker exec -it predmaint_postgres psql -U predmaint -d predictive_maintenance_db -f /path/to/database/schema.sql
```

### 4. Train the model

Run the notebooks in order (`01` → `05`), or run the training scripts in
`src/ml/` directly, to produce a trained model in `models/`.

### 5. Load sensor data into the database

```bash
cd src/db
python load_to_db.py
```

### 6. Run the API

```bash
cd src/api
uvicorn main:app --reload
```

API docs available at `http://localhost:8000/docs`.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/predictions/latest` | Latest prediction per engine, with maintenance status |
| GET | `/predictions/history/{engine_id}` | Full prediction history for one engine |
| POST | `/predictions/{engine_id}` | Run a new prediction for one engine |
| GET | `/simulations/{simulation_id}` | Cycle-by-cycle results of a simulation run |

## Model

XGBoost regressor trained on rolling-window sensor features (mean/std over
5 and 10 cycles), with RUL capped at 125 cycles (piecewise linear
degradation assumption, standard practice on this dataset).
