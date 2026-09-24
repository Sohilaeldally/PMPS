"""
Data cleaning & preprocessing for NASA C-MAPSS (FD001).
"""

import pandas as pd


COLUMN_NAMES = (
    [
        "unit_number",
        "time_cycles",
        "op_setting_1",
        "op_setting_2",
        "op_setting_3",
    ]
    + [f"sensor_{i}" for i in range(1, 22)]
)


def load_raw_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        sep=r"\s+",
        header=None
    )

    df.columns = COLUMN_NAMES

    return df


def add_rul_train(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    max_cycles = (
        df.groupby("unit_number")["time_cycles"]
        .transform("max")
    )

    df["RUL"] = max_cycles - df["time_cycles"]

    return df


def add_rul_test(df: pd.DataFrame,rul_path: str) -> pd.DataFrame:
    df = df.copy()

    rul_test = pd.read_csv(
        rul_path,
        header=None
    )

    last_cycles = (
        df.groupby("unit_number")["time_cycles"]
        .max()
        .reset_index()
    )

    last_cycles.columns = [
        "unit_number",
        "last_cycle"
    ]

    last_cycles["true_RUL"] = rul_test[0]

    last_cycles["failure_cycle"] = (
        last_cycles["last_cycle"]
        + last_cycles["true_RUL"]
    )

    df = df.merge(
        last_cycles[
            ["unit_number", "failure_cycle"]
        ],
        on="unit_number"
    )

    df["RUL"] = (
        df["failure_cycle"]
        - df["time_cycles"]
    )

    df = df.drop(
        columns=["failure_cycle"]
    )

    return df



def cap_rul(df: pd.DataFrame, cap: int = 125) -> pd.DataFrame:
 
    df = df.copy()
    df["RUL"] = df["RUL"].clip(upper=cap)
    return df



def get_constant_columns(
    df: pd.DataFrame
) -> list:
    return [
        col
        for col in df.columns
        if df[col].nunique() <= 1
    ]


def get_feature_columns(df: pd.DataFrame,drop_cols: list = None) -> list:

    drop_cols = drop_cols or []

    constant_cols = get_constant_columns(df)

    exclude = set(
        constant_cols
        + drop_cols
        + ["RUL", "unit_number"]
    )

    return [
        col
        for col in df.columns
        if col not in exclude
    ]

def clean_train_pipeline(raw_path: str) -> pd.DataFrame:

    df = load_raw_data(raw_path)
    df = add_rul_train(df)

    return df


def clean_test_pipeline(raw_path: str,rul_path: str) -> pd.DataFrame:

    df = load_raw_data(raw_path)
    df = add_rul_test(df, rul_path)

    return df