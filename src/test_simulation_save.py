
import uuid

from db.queries import get_engine_history, save_simulation_predictions
from ml.predict import load_model, simulate_engine_history


engine_id = 1
simulation_id = uuid.uuid4()

engine_data = get_engine_history(engine_id)
simulation_df = simulate_engine_history(engine_data, model=load_model())

save_simulation_predictions(
    simulation_id=simulation_id,
    engine_id=engine_id,
    simulation_df=simulation_df,
)

print("Simulation ID:", simulation_id)
print("Engine ID:", engine_id)
print("Rows generated:", len(simulation_df))
print(simulation_df.tail())
