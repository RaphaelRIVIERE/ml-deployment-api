import joblib
from pathlib import Path

MODEL_PATH = Path("ml_model/best_pipeline.pkl")


def load_pipeline():
    data = joblib.load(MODEL_PATH)
    return data["pipeline"], data["threshold"]
