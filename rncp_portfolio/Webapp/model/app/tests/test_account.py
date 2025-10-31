from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_id_fetch_valid():
    response = client.post("/account/id_fetch", json={"token": "mocktoken"})
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data or isinstance(data, int)
