import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader
from app.schemas.prediction import PredictionInput, PredictionOutput
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import crud

router = APIRouter()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(request: Request, api_key: str = Security(api_key_header)):
    if not api_key or api_key != request.app.state.settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Clé API manquante ou invalide")


@router.get("/health", summary="Health check", description="Vérifie que l'API est opérationnelle")
def health_check():
    return {"status": "ok", "message": "API opérationnelle"}


@router.get("/model/info", summary="Informations sur le modèle", description="Retourne les métadonnées du modèle déployé", dependencies=[Depends(verify_api_key)])
def model_info(request: Request):
    return {
        "algorithme": "Régression Logistique",
        "seuil": request.app.state.threshold,
        "description": "Classification binaire — risque de départ RH (0 = Reste, 1 = Quitte)",
    }


@router.post("/predict", response_model=PredictionOutput, summary="Prédiction du risque de départ", description="Envoie les features RH d'un employé et reçoit une prédiction", dependencies=[Depends(verify_api_key)])
def predict_churn(data: PredictionInput, request: Request, db: Session = Depends(get_db)):
    pipeline = request.app.state.pipeline
    threshold = request.app.state.threshold
    df = pd.DataFrame([data.model_dump()])
    proba = float(pipeline.predict_proba(df)[0][1])
    prediction = int(proba >= threshold)
    label = "Quitte" if prediction == 1 else "Reste"
    output = PredictionOutput(prediction=prediction, label=label, probabilite=round(proba, 4))
    crud.log_prediction(db, data, output)
    return output