from fastapi.testclient import TestClient

from api import app

client = TestClient(app)

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "Ok"}

def test_list_cameras():
    response = client.get("/cameras")
    assert response.status_code == 200
    assert type(response.json()) == list

def test_list_create_camera():
    response = client.post("/cameras")
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_get_camera():
    response = client.get("/cameras/1")
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_delete_camera():
    response = client.delete("/cameras/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Delete camera device"}
