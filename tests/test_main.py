from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/home")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Backend Running"
    }

def test_get_jobs():
    response = client.get("/jobs")

    assert response.status_code == 200

def test_get_missing_jon():
    response = client.get("job/99999")

    assert response.status_code == 404