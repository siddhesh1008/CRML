import pytest


def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["mqtt_connected"] is True
    assert "version" in data


def test_health_mqtt_disconnected(store, registry):
    from unittest.mock import MagicMock
    from fastapi.testclient import TestClient
    from crml.api.app import app, attach_bridge, attach_registry, attach_store

    bridge = MagicMock()
    bridge.is_connected = False
    attach_bridge(bridge)
    attach_registry(registry)
    attach_store(store)

    r = TestClient(app).get("/health")
    assert r.json()["mqtt_connected"] is False


def test_models_empty(client):
    r = client.get("/models")
    assert r.status_code == 200
    assert r.json() == []


def test_models_with_entries(client, registry):
    registry.register("perception", "1.0.0", "perception", "p.pt")
    r = client.get("/models")
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["name"] == "perception"


def test_inference_no_model(client):
    r = client.post("/inference/rover", json={"task": "perception", "data": {}})
    assert r.status_code == 404


def test_inference_with_model(client, registry, tmp_path):
    model_file = tmp_path / "model.pt"
    model_file.write_text("fake")
    registry.register("perception", "1.0.0", "perception", str(model_file))
    r = client.post("/inference/rover", json={"task": "perception", "data": {"frame": 1}})
    assert r.status_code == 200
    data = r.json()
    assert data["robot_id"] == "rover"
    assert data["task"] == "perception"


def test_data_stats_empty(client):
    r = client.get("/data/stats")
    assert r.status_code == 200
    assert r.json() == {}


def test_data_stats_with_data(client, store):
    store.record("rover", "status", {"battery": 90})
    r = client.get("/data/stats")
    assert r.status_code == 200
    assert r.json()["rover"]["status"] == 1
