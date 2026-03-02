import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.db.session import get_database_url

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(get_database_url()))
from app.db.models import Employee, Prediction
from app.routes.predict import _compute_features
from ml_model.loader import load_pipeline


def stats_employees(session):
    total = session.query(Employee).count()
    print(f"\n--- Employés en base ---")
    print(f"Total : {total}")

    quittes = session.query(Employee).filter(Employee.a_quitte_l_entreprise == True).count()
    print(f"Ont quitté : {quittes} ({round(quittes / total * 100, 1)}%)")


def apercu_employees(session, n=5):
    rows = session.query(Employee).limit(n).all()
    print(f"\n--- Aperçu ({n} premiers employés) ---")
    for e in rows:
        print(f"  id={e.id} | {e.poste} | {e.statut_marital} | quitte={e.a_quitte_l_entreprise}")


def predict_from_db(session, employee_id: int):
    pipeline, threshold = load_pipeline()

    emp = session.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        print(f"Employé id={employee_id} introuvable.")
        return

    data = {col: getattr(emp, col) for col in [
        "age", "genre", "statut_marital", "poste", "domaine_etude",
        "niveau_education", "nombre_experiences_precedentes", "annee_experience_totale",
        "annees_dans_l_entreprise", "annees_dans_le_poste_actuel",
        "annees_sous_responsable_actuel", "annees_depuis_la_derniere_promotion",
        "note_evaluation_actuelle", "note_evaluation_precedente",
        "augmentation_salaire_precedente", "nb_formations_suivies",
        "nombre_participation_pee", "satisfaction_employee_environnement",
        "satisfaction_employee_nature_travail", "satisfaction_employee_equipe",
        "satisfaction_employee_equilibre_pro_perso", "heure_supplementaires",
        "frequence_deplacement", "distance_domicile_travail", "revenu_mensuel",
    ]}

    df = _compute_features(pd.DataFrame([data]))
    proba = float(pipeline.predict_proba(df)[0][1])
    prediction = int(proba >= threshold)
    label = "Quitte" if prediction == 1 else "Reste"

    print(f"\n--- Prédiction pour l'employé id={employee_id} ---")
    print(f"  Poste : {emp.poste} | Réel : {'Quitte' if emp.a_quitte_l_entreprise else 'Reste'}")
    print(f"  Prédit : {label} (probabilité : {round(proba, 4)})")


def stats_predictions(session):
    total = session.query(Prediction).count()
    print(f"\n--- Prédictions loggées en base ---")
    print(f"Total : {total}")
    if total > 0:
        derniere = session.query(Prediction).order_by(Prediction.id.desc()).first()
        print(f"Dernière : id={derniere.id} | {derniere.label} | proba={derniere.probabilite} | {derniere.created_at}")


if __name__ == "__main__":
    session = SessionLocal()
    try:
        stats_employees(session)
        apercu_employees(session, n=5)
        predict_from_db(session, employee_id=1)
        stats_predictions(session)
    finally:
        session.close()
