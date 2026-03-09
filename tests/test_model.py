import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from ml_model.loader import load_pipeline
from app.main import app
from tests.conftest import VALID_PAYLOAD, TEST_API_KEY, TEST_API_KEY_HASH


# Fixture : client avec le VRAI pipeline (pas de mock)
@pytest.fixture(scope="module")
def real_client():
    with patch.dict("os.environ", {"API_KEY": TEST_API_KEY_HASH}), \
         patch("app.middleware.logging.crud.log_request"):
        with TestClient(app) as c:
            yield c


# Tester que le pipeline .pkl se charge correctement
def test_load_pipeline():
    pipeline, threshold = load_pipeline()
    assert pipeline is not None
    assert isinstance(threshold, float)


# Tester que la prédiction retourne bien "Reste" ou "Quitte"
def test_predict_label_valid(real_client):
    response = real_client.post(
        "/predict",
        json=VALID_PAYLOAD,
        headers={"X-API-Key": TEST_API_KEY},
    )
    assert response.status_code == 200
    assert response.json()["label"] in ("Reste", "Quitte")


# Tester que la probabilité est bien comprise entre 0 et 1
def test_predict_probabilite_range(real_client):
    response = real_client.post(
        "/predict",
        json=VALID_PAYLOAD,
        headers={"X-API-Key": TEST_API_KEY},
    )
    assert 0.0 <= response.json()["probabilite"] <= 1.0


# Tester que le seuil 0.40 est bien appliqué
@pytest.mark.parametrize("proba_quitte,expected_label", [
    (0.50, "Quitte"),  # clairement au-dessus du seuil
    (0.30, "Reste"),   # clairement en-dessous du seuil
])
def test_threshold_applied(proba_quitte, expected_label):
    _, threshold = load_pipeline()  # ← vrai seuil (0.3999...7)
    mock_pipeline = MagicMock()
    mock_pipeline.predict_proba.return_value = [[1 - proba_quitte, proba_quitte]]

    with patch("app.main.load_pipeline", return_value=(mock_pipeline, threshold)), \
         patch.dict("os.environ", {"API_KEY": TEST_API_KEY_HASH}), \
         patch("app.middleware.logging.crud.log_request"):
        with TestClient(app) as c:
            response = c.post(
                "/predict",
                json=VALID_PAYLOAD,
                headers={"X-API-Key": TEST_API_KEY},
            )

    assert response.json()["label"] == expected_label

