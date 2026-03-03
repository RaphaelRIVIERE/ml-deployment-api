import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from ml_model.loader import load_pipeline

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "data_merged.csv")
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "examples", "predictions_sample.csv")

N_SAMPLES = 10


def generate():
    pipeline, threshold = load_pipeline()

    df = pd.read_csv(CSV_PATH).head(N_SAMPLES)
    inputs = df.drop(columns=["a_quitte_l_entreprise"])

    probas = pipeline.predict_proba(inputs.copy())[:, 1]
    predictions = (probas >= threshold).astype(int)

    inputs["prediction"] = predictions
    inputs["probabilite"] = probas.round(4)
    inputs["label"] = ["Quitte" if p == 1 else "Reste" for p in predictions]

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    inputs.to_csv(OUTPUT_PATH, index=False)
    print(f"Fichier généré : {OUTPUT_PATH} ({N_SAMPLES} lignes)")


if __name__ == "__main__":
    generate()
