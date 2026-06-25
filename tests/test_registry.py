import pytest
from pathlib import Path
from crml.registry.registry import ModelRegistry


def test_start_empty(tmp_path):
    r = ModelRegistry(tmp_path / "models")
    r.start()
    assert r.list() == []
    assert (tmp_path / "models" / "registry.json").exists()


def test_register(registry):
    entry = registry.register("perception", "1.0.0", "perception", "models/p.pt")
    assert entry.name == "perception"
    assert entry.version == "1.0.0"
    assert entry.task == "perception"


def test_list(registry):
    registry.register("model-a", "1.0.0", "perception", "a.pt")
    registry.register("model-b", "1.0.0", "motion", "b.pt")
    assert len(registry.list()) == 2


def test_get_by_version(registry):
    registry.register("perception", "1.0.0", "perception", "v1.pt")
    registry.register("perception", "2.0.0", "perception", "v2.pt")
    entry = registry.get("perception", "1.0.0")
    assert entry.version == "1.0.0"


def test_get_latest(registry):
    registry.register("perception", "1.0.0", "perception", "v1.pt")
    registry.register("perception", "2.0.0", "perception", "v2.pt")
    entry = registry.get("perception", "latest")
    assert entry.version == "2.0.0"


def test_get_missing(registry):
    assert registry.get("nonexistent") is None


def test_manifest_persisted(tmp_path):
    models_dir = tmp_path / "models"
    r1 = ModelRegistry(models_dir)
    r1.start()
    r1.register("perception", "1.0.0", "perception", "p.pt")

    r2 = ModelRegistry(models_dir)
    r2.start()
    assert len(r2.list()) == 1
    assert r2.list()[0].name == "perception"


def test_load_missing_file(registry):
    registry.register("perception", "1.0.0", "perception", "nonexistent.pt")
    result = registry.load("perception")
    assert result is None


def test_load_existing_file(registry, tmp_path):
    model_file = tmp_path / "model.pt"
    model_file.write_text("fake model")
    registry.register("perception", "1.0.0", "perception", str(model_file))
    result = registry.load("perception")
    assert result is not None
