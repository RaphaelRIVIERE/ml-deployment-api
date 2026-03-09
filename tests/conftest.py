import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db
import hashlib


TEST_API_KEY = "test-secret-key"
TEST_API_KEY_HASH = hashlib.sha256(TEST_API_KEY.encode()).hexdigest()


VALID_PAYLOAD = {
    "age": 35, "genre": "M", "statut_marital": "Marié(e)",
    "poste": "Consultant", "domaine_etude": "Infra & Cloud",
    "niveau_education": 3, "departement": "Ventes", "niveau_hierarchique_poste": 2,
    "nombre_experiences_precedentes": 2,
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
    "heure_supplementaires": "Non", "frequence_deplacement": "Occasionnel",
    "distance_domicile_travail": 10, "revenu_mensuel": 5000,
}

def override_get_db():
    yield MagicMock()
    
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    mock_pipeline = MagicMock()
    # Simule predict_proba → [[proba_reste, proba_quitte]]
    # 0.3 < seuil 0.40 → prédiction "Reste"
    mock_pipeline.predict_proba.return_value = [[0.70, 0.30]]

    with (
        # remplace le vrai .pkl par le pipeline mocké
        patch("app.main.load_pipeline", return_value=(mock_pipeline, 0.40)),
        # injecte le hash de la clé de test
        patch.dict("os.environ", {"API_KEY": TEST_API_KEY_HASH}),
        # évite les écritures en DB pendant les tests
        patch("app.middleware.logging.crud.log_request"),
    ):
        with TestClient(app) as c:
               yield c
