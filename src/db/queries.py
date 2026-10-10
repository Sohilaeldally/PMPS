import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
import psycopg2

from config import DB_CONFIG


def get_engine_history(engine_id: int) -> pd.DataFrame:
    conn = psycopg2.connect(**DB_CONFIG)

    query = """
        SELECT *
        FROM sensor_readings
        WHERE engine_id = %s
        ORDER BY cycle
    """

    df = pd.read_sql(
        query,
        conn,
        params=(engine_id,)
    )

    conn.close()

    return df


def save_prediction(engine_id: int, predicted_rul: float) -> None:
    conn = psycopg2.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO predictions (engine_id, predicted_rul)
                VALUES (%s, %s)
                """,
                (engine_id, predicted_rul)
            )

        conn.commit()

    finally:
        conn.close()    