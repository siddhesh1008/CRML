import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from crml.pipeline.store import DataStore
from crml.registry.registry import ModelRegistry
from crml.api.app import app, attach_bridge, attach_registry, attach_store


@pytest.fixture
def store(tmp_path):
    return DataStore(tmp_path / "data")


@pytest.fixture
def registry(tmp_path):
    r = ModelRegistry(tmp_path / "models")
    r.start()
    return r


@pytest.fixture
def mock_bridge():
    bridge = MagicMock()
    bridge.is_connected = True
    return bridge


@pytest.fixture
def client(store, registry, mock_bridge):
    attach_bridge(mock_bridge)
    attach_registry(registry)
    attach_store(store)
    return TestClient(app)
