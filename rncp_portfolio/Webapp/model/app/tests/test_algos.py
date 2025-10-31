from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_best_categories_returns_structure(monkeypatch):
    def mock_run_with_id_list_limit(pro_id, limit):
        return [
            {"final_score": 50000, "categories": [
                {"name": "geriatrie"}, {"name": "day"}]}
        ]
    monkeypatch.setattr("app.main.run_with_id_list_limit",
                        mock_run_with_id_list_limit)
    response = client.post("/algos/best_categories",
                           json={"professional_id": 1})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "categories" in response.json()[0]
