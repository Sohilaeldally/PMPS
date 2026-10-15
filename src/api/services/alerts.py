def get_maintenance_status(predicted_rul: float) -> str:
    if predicted_rul <= 10:
        return "CRITICAL"
    elif predicted_rul <= 60:   
        return "WARNING"
    return "NORMAL"