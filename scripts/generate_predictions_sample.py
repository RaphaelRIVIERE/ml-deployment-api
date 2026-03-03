import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.db.models import Employee
from ml_model.loader import load_pipeline
from app.schemas.prediction import PredictionInput


EXAMPLES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "examples")
INPUT_PATH = os.path.join(EXAMPLES_DIR, "input_sample.csv")
OUTPUT_PATH = os.path.join(EXAMPLES_DIR, "output_sample.csv")

N_SAMPLES = 10

FEATURE_COLUMNS = list(PredictionInput.model_fields.keys())


def generate():
    db_url = (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(db_url))
    session = SessionLocal()

    try:
        rows = session.query(Employee).limit(N_SAMPLES).all()
        inputs = pd.DataFrame(
            [{col: getattr(e, col) for col in FEATURE_COLUMNS} for e in rows]
        )
    finally:
        session.close()

    pipeline, threshold = load_pipeline()
    probas = pipeline.predict_proba(inputs.copy())[:, 1]
    predictions = (probas >= threshold).astype(int)

    os.makedirs(EXAMPLES_DIR, exist_ok=True)

    inputs.to_csv(INPUT_PATH, index=False)
    print(f"Fichier généré : {INPUT_PATH} ({N_SAMPLES} lignes)")

    outputs = pd.DataFrame({
        "prediction": predictions,
        "label": ["Quitte" if p == 1 else "Reste" for p in predictions],
        "probabilite": probas.round(4),
    })
    outputs.to_csv(OUTPUT_PATH, index=False)
    print(f"Fichier généré : {OUTPUT_PATH} ({N_SAMPLES} lignes)")


if __name__ == "__main__":
    generate()
