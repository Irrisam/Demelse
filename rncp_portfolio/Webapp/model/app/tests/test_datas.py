from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_pros_returns_pro_list(monkeypatch):
    def mock_get_pros_list(user_id):
        return [{"id": 1, "firstname": "Jean", "lastname": "Dupont", "email": "jean@example.com"}]
    monkeypatch.setattr("app.main.get_pros_list", mock_get_pros_list)

    response = client.post("/datas/list/pros", json={"userId": 19})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["firstname"] == "Jean"
