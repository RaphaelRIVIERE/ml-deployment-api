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


@router.get("/", tags=["Général"], summary="Accueil de l'API", description="Retourne les informations générales de l'API.")
def root(request: Request):
    return {
        "name": request.app.title,
        "version": request.app.version,
        "documentation": str(request.base_url) + "docs",
        "health": str(request.base_url) + "health",
    }


@router.get("/health", tags=["Monitoring"], summary="Vérification de l'état de l'API", description="Retourne le statut de l'API. Aucune authentification requise.")
def health_check():
    return {"status": "ok", "message": "API opérationnelle"}


@router.get("/model/info", tags=["Prédictions"], summary="Informations sur le modèle", description="Retourne l'algorithme utilisé, le seuil de décision et une description du modèle déployé.", dependencies=[Depends(verify_api_key)])
def model_info(request: Request):
    return {
        "algorithme": "Régression Logistique",
        "seuil": request.app.state.threshold,
        "description": "Classification binaire — risque de départ RH (0 = Reste, 1 = Quitte)",
    }


@router.post("/predict", tags=["Prédictions"], response_model=PredictionOutput, response_description="Soumet les données RH d'un employé au modèle et retourne une prédiction de départ. Chaque appel est enregistré en base de données.", summary="Prédiction du risque de départ", description="Envoie les features RH d'un employé et reçoit une prédiction", dependencies=[Depends(verify_api_key)])
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