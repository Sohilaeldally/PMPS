import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
import psycopg2

from preprocessing import COLUMN_NAMES
from config import DB_CONFIG


DATA_PATH = "../data/test_FD001.txt"


def load_data():
    df = pd.read_csv(
        DATA_PATH,
        sep=r"\s+",
        header=None,
        names=COLUMN_NAMES
    )

    return df


def insert_data(df):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    query = """
        INSERT INTO sensor_readings (
            engine_id,
            cycle,
            op_setting_1,
            op_setting_2,
            op_setting_3,
            sensor_1,
            sensor_2,
            sensor_3,
            sensor_4,
            sensor_5,
            sensor_6,
            sensor_7,
            sensor_8,
            sensor_9,
            sensor_10,
            sensor_11,
            sensor_12,
            sensor_13,
            sensor_14,
            sensor_15,
            sensor_16,
            sensor_17,
            sensor_18,
            sensor_19,
            sensor_20,
            sensor_21
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
    """

    rows = [
        tuple(row)
        for row in df.itertuples(index=False, name=None)
    ]

    cursor.executemany(query, rows)

    conn.commit()

    cursor.close()
    conn.close()

    print(f"Inserted {len(rows)} rows into sensor_readings.")


if __name__ == "__main__":
    data = load_data()

    print("Data shape:", data.shape)

    insert_data(data)