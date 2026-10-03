from pathlib import Path

from xgboost import XGBRegressor

from preprocessing import (
    clean_train_rolling_pipeline,
    cap_rul,
    get_feature_columns
)

from config import (
    ROLLING_SENSORS,
    ROLLING_WINDOWS
)


train = clean_train_rolling_pipeline(
    "../data/train_FD001.txt",
    sensors=ROLLING_SENSORS,
    windows=ROLLING_WINDOWS
)

train = cap_rul(
    train,
    cap=125
)

feature_cols = get_feature_columns(train)

X = train[feature_cols]
y = train["RUL"]

print("Training shape:", X.shape)
print("Number of features:", len(feature_cols))
print("RUL max after cap:", y.max())


final_model = XGBRegressor(
    n_estimators=200,
    learning_rate=0.02,
    max_depth=3,
    min_child_weight=3,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

final_model.fit(X, y)


models_dir = Path("../models")
models_dir.mkdir(exist_ok=True)

model_path = models_dir / "final_xgboost_v3.json"

final_model.get_booster().save_model(model_path)

print(f"Model v3 saved to: {model_path}")