"""
Training utilities for the Predictive Maintenance project.
"""

from sklearn.model_selection import train_test_split


def split_by_engine(df,test_size: float = 0.2,random_state: int = 42):
    engine_ids = df["unit_number"].unique()

    train_engines, val_engines = train_test_split(
        engine_ids,
        test_size=test_size,
        random_state=random_state
    )

    train_data = df[df["unit_number"].isin(train_engines)].copy()

    val_data = df[df["unit_number"].isin(val_engines)].copy()

    return train_data, val_data