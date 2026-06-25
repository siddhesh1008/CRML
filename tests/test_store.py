import json
from crml.pipeline.store import DataStore


def test_record_creates_file(store, tmp_path):
    store.record("rover", "status", {"battery": 90})
    files = list((tmp_path / "data" / "raw").rglob("status.jsonl"))
    assert len(files) == 1


def test_record_appends(store, tmp_path):
    store.record("rover", "status", {"battery": 90})
    store.record("rover", "status", {"battery": 80})
    files = list((tmp_path / "data" / "raw").rglob("status.jsonl"))
    lines = files[0].read_text().strip().splitlines()
    assert len(lines) == 2


def test_record_entry_has_timestamp(store, tmp_path):
    store.record("rover", "status", {"battery": 90})
    files = list((tmp_path / "data" / "raw").rglob("status.jsonl"))
    entry = json.loads(files[0].read_text().strip())
    assert "ts" in entry
    assert "data" in entry


def test_record_multiple_robots(store, tmp_path):
    store.record("rover", "status", {"battery": 90})
    store.record("arm", "status", {"joint": 45})
    robot_dirs = list((tmp_path / "data" / "raw").rglob("status.jsonl"))
    assert len(robot_dirs) == 2


def test_stats_empty(store):
    assert store.stats() == {}


def test_stats_counts(store):
    store.record("rover", "status", {"battery": 90})
    store.record("rover", "status", {"battery": 80})
    store.record("rover", "sensors_camera", {"objects": []})
    stats = store.stats()
    assert stats["rover"]["status"] == 2
    assert stats["rover"]["sensors_camera"] == 1
