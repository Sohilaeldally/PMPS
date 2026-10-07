from os import environ

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

ROLLING_SENSORS = [
    "sensor_11",
    "sensor_4",
    "sensor_12",
    "sensor_7"
]

ROLLING_WINDOWS = [5, 10]


MODEL_FEATURES = [
    "time_cycles",
    "op_setting_1",
    "op_setting_2",
    "sensor_2",
    "sensor_3",
    "sensor_4",
    "sensor_6",
    "sensor_7",
    "sensor_8",
    "sensor_9",
    "sensor_11",
    "sensor_12",
    "sensor_13",
    "sensor_14",
    "sensor_15",
    "sensor_17",
    "sensor_20",
    "sensor_21",
    "sensor_11_roll_mean_5",
    "sensor_11_roll_std_5",
    "sensor_11_roll_mean_10",
    "sensor_11_roll_std_10",
    "sensor_4_roll_mean_5",
    "sensor_4_roll_std_5",
    "sensor_4_roll_mean_10",
    "sensor_4_roll_std_10",
    "sensor_12_roll_mean_5",
    "sensor_12_roll_std_5",
    "sensor_12_roll_mean_10",
    "sensor_12_roll_std_10",
    "sensor_7_roll_mean_5",
    "sensor_7_roll_std_5",
    "sensor_7_roll_mean_10",
    "sensor_7_roll_std_10",
]

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "predictive_maintenance_db",
    "user": "predmaint",
    "password": environ.get("DB_PASSWORD", "predmaint_password"),
}