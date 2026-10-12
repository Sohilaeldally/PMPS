import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
import psycopg2

from config import DB_CONFIG

from uuid import UUID

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


def get_latest_prediction(engine_id: int):
    conn = psycopg2.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, engine_id, predicted_rul, prediction_time
                FROM predictions
                WHERE engine_id = %s
                ORDER BY prediction_time DESC, id DESC
                LIMIT 1
                """,
                (engine_id,)
            )

            return cursor.fetchone()

    finally:
        conn.close()


def get_latest_predictions():
    conn = psycopg2.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT DISTINCT ON (engine_id)
                    id,
                    engine_id,
                    predicted_rul,
                    prediction_time
                FROM predictions
                ORDER BY engine_id, prediction_time DESC, id DESC
                """
            )

            return cursor.fetchall()

    finally:
        conn.close()

def get_prediction_history(engine_id: int):
    conn = psycopg2.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, engine_id, predicted_rul, prediction_time
                FROM predictions
                WHERE engine_id = %s
                ORDER BY prediction_time ASC, id ASC
                """,
                (engine_id,)
            )

            return cursor.fetchall()

    finally:
        conn.close()


def save_simulation_predictions(
    simulation_id: UUID,
    engine_id: int,
    simulation_df: pd.DataFrame,
    actual_rul: float | None = None,
) -> None:
    """
    Save cycle-by-cycle simulated predictions separately
    from the production predictions table.
    """
    conn = psycopg2.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            rows = [
                (
                    str(simulation_id),
                    engine_id,
                    int(row.cycle),
                    float(row.predicted_rul),
                    (
                        actual_rul + (int(simulation_df["cycle"].max()) - int(row.cycle))
                        if actual_rul is not None
                        else None
                    ),
                )
                for row in simulation_df.itertuples(index=False)
            ]

            cursor.executemany(
                """
                INSERT INTO simulation_predictions
                    (simulation_id, engine_id, cycle, predicted_rul, actual_rul)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (simulation_id, engine_id, cycle) DO NOTHING
                """,
                rows,
            )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()




def get_simulation_predictions(simulation_id: str):
    conn = psycopg2.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    simulation_id,
                    engine_id,
                    cycle,
                    predicted_rul,
                    actual_rul,
                    data_source,
                    created_at
                FROM simulation_predictions
                WHERE simulation_id = %s
                ORDER BY engine_id, cycle
                """,
                (simulation_id,)
            )

            columns = [desc[0] for desc in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

    finally:
        conn.close()
