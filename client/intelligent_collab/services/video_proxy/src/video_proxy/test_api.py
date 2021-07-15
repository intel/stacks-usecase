from fastapi.testclient import TestClient

import config
import api

client = TestClient(config.app)

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "Ok"}

def test_get_service():
    response = client.get("/service")
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_get_stream_type():
    response = client.get("/stream_type")
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_get_video_source():
    response = client.get("/video_source")
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_get_virtual_device():
    response = client.get("/virtual_device")
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_set_virtual_device():
    response = client.post("/virtual_device/1")
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_get_virtual_device():
    response = client.get("/virtual_device")
    assert response.status_code == 200
    assert type(response.json()) == dict
