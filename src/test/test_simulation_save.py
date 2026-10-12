
import uuid

from db.queries import get_engine_history, save_simulation_predictions
from ml.predict import load_model, simulate_engine_history

engine_id = 1
simulation_id = uuid.uuid4()

print("Loading engine history...", flush=True)
engine_data = get_engine_history(engine_id)

print(f"Loaded {len(engine_data)} cycles.", flush=True)
print("Loading model...", flush=True)
model = load_model()

print("Running simulation; this may take a little while...", flush=True)
simulation_df = simulate_engine_history(engine_data, model=model)

print(f"Simulation complete: {len(simulation_df)} predictions.", flush=True)
print("Saving predictions to database...", flush=True)

save_simulation_predictions(
    simulation_id=simulation_id,
    engine_id=engine_id,
    simulation_df=simulation_df,
)

print("Saved successfully!", flush=True)
print("Simulation ID:", simulation_id, flush=True)
print(simulation_df.tail(), flush=True)
