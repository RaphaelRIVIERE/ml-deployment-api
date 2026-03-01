import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app

TEST_API_KEY = "test-secret-key"

VALID_PAYLOAD = {
    "age": 35, "genre": 1, "statut_marital": "Marié(e)",
    "poste": "Consultant", "domaine_etude": "Infra & Cloud",
    "niveau_education": 3, "nombre_experiences_precedentes": 2,
    "annee_experience_totale": 10, "annees_dans_l_entreprise": 5,
    "annees_dans_le_poste_actuel": 2, "annees_sous_responsable_actuel": 3,
    "annees_depuis_la_derniere_promotion": 1,
    "note_evaluation_actuelle": 3, "note_evaluation_precedente": 3,
    "augmentation_salaire_precedente": 15, "nb_formations_suivies": 2,
    "nombre_participation_pee": 1,
    "satisfaction_employee_environnement": 3,
    "satisfaction_employee_nature_travail": 4,
    "satisfaction_employee_equipe": 3,
    "satisfaction_employee_equilibre_pro_perso": 2,
    "heure_supplementaires": 0, "frequence_deplacement": 1,
    "distance_domicile_travail": 10, "revenu_mensuel": 5000,
}

@pytest.fixture(scope="module")
def client():
    mock_pipeline = MagicMock()
    # Simule predict_proba → [[proba_reste, proba_quitte]]
    # 0.3 < seuil 0.40 → prédiction "Reste"
    mock_pipeline.predict_proba.return_value = [[0.70, 0.30]]

    with patch("app.main.load_pipeline", return_value=(mock_pipeline, 0.40)), \
         patch.dict("os.environ", {"API_KEY": TEST_API_KEY}):
        with TestClient(app) as c:
            yield c
