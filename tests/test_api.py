from tests.conftest import VALID_PAYLOAD, TEST_API_KEY


# Tester GET /health
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# Tester POST /predict avec données valides
def test_predict_valid(client):
    response = client.post(
        "/predict",
        json=VALID_PAYLOAD,
        headers={"X-API-Key": TEST_API_KEY},
    )
    assert response.status_code == 200
    body = response.json()
    assert "label" in body
    assert body["label"] in ("Reste", "Quitte")
    assert "probabilite" in body
    assert 0.0 <= body["probabilite"] <= 1.0


# Tester POST /predict avec données invalides
def test_predict_invalid_data(client):
    invalid_payload = {"age": 999, "genre": 99}  # hors bornes + champs manquants
    response = client.post(
        "/predict",
        json=invalid_payload,
        headers={"X-API-Key": TEST_API_KEY},
    )
    assert response.status_code == 422  # Pydantic validation error


# Tester POST /predict sans API Key → 401
def test_predict_no_api_key(client):
    response = client.post("/predict", json=VALID_PAYLOAD)
    assert response.status_code == 401


# Tester GET /predictions avec API Key valide
def test_get_predictions_authenticated(client):
    response = client.get(
        "/predictions",
        headers={"X-API-Key": TEST_API_KEY},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Tester GET /predictions sans API Key → 401
def test_get_predictions_no_api_key(client):
    response = client.get("/predictions")
    assert response.status_code == 401
