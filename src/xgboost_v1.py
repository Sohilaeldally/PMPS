from pathlib import Path

from xgboost import XGBRegressor

from preprocessing import clean_train_pipeline, get_feature_columns


train = clean_train_pipeline(
    "../data/train_FD001.txt"
)


feature_cols = get_feature_columns(train)


X = train[feature_cols]
y = train["RUL"]

final_model = XGBRegressor(
    n_estimators=200,
    learning_rate=0.03,
    max_depth=4,
    min_child_weight=3,
    subsample=1.0,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

final_model.fit(X, y)


models_dir = Path("../models")
models_dir.mkdir(exist_ok=True)

model_path = models_dir / "final_xgboost.json"

final_model.get_booster().save_model(model_path)

print(f"Model saved to: {model_path}")