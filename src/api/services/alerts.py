def get_maintenance_status(predicted_rul: float) -> str:
    if predicted_rul <= 15:
        return "CRITICAL"
    elif predicted_rul <= 30:   
        return "WARNING"
    return "NORMAL"