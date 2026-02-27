import numpy as np
import pandas as pd
from fastapi import APIRouter, Request
from app.schemas.prediction import PredictionInput, PredictionOutput

router = APIRouter()

SAT_COLS = [
    "satisfaction_employee_environnement",
    "satisfaction_employee_nature_travail",
    "satisfaction_employee_equipe",
    "satisfaction_employee_equilibre_pro_perso",
]


# TODO: intégrer ce feature engineering comme premier step du pipeline sklearn
# pour éviter de devoir maintenir ce code en sync avec le script d'entraînement.
def _compute_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["stabilite_management"] = df["annees_sous_responsable_actuel"] / (df["annees_dans_le_poste_actuel"] + 1)
    df["flag_surcharge_et_deplacement"] = (
        (df["heure_supplementaires"] == 1) & (df["frequence_deplacement"] == 2)
    ).astype(int)
    df["ratio_promotion_anciennete"] = (
        df["annees_depuis_la_derniere_promotion"] / (df["annees_dans_l_entreprise"] + 1)
    )
    df["satisfaction_globale"] = df[SAT_COLS].sum(axis=1)
    df["satisfaction_min"] = df[SAT_COLS].min(axis=1)
    df["log_revenu"] = np.log1p(df["revenu_mensuel"])
    df = df.drop(columns=["annees_sous_responsable_actuel", "annees_depuis_la_derniere_promotion", "revenu_mensuel"])
    return df


@router.get("/health", summary="Health check", description="Vérifie que l'API est opérationnelle")
def health_check():
    return {"status": "ok", "message": "API opérationnelle"}


@router.get("/model/info", summary="Informations sur le modèle", description="Retourne les métadonnées du modèle déployé")
def model_info(request: Request):
    return {
        "algorithme": "Régression Logistique",
        "seuil": request.app.state.threshold,
        "description": "Classification binaire — risque de départ RH (0 = Reste, 1 = Quitte)",
    }


@router.post("/predict", response_model=PredictionOutput, summary="Prédiction du risque de départ", description="Envoie les features RH d'un employé et reçoit une prédiction")
def predict_churn(data: PredictionInput, request: Request):
    pipeline = request.app.state.pipeline
    threshold = request.app.state.threshold
    df = _compute_features(pd.DataFrame([data.model_dump()]))
    proba = float(pipeline.predict_proba(df)[0][1])
    prediction = int(proba >= threshold)
    label = "Quitte" if prediction == 1 else "Reste"
    return PredictionOutput(prediction=prediction, label=label, probabilite=round(proba, 4))
