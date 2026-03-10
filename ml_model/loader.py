import joblib
from pathlib import Path

MODEL_PATH = Path("ml_model/pipeline.pkl")


def load_pipeline():
    # Retourne le pipeline sklearn et le seuil de décision depuis le fichier .pkl
    data = joblib.load(MODEL_PATH)
    return data["pipeline"], data["threshold"]
