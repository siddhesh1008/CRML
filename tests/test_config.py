import pytest
from pathlib import Path
from crml.config.settings import Settings, MqttSettings, ApiSettings, CrmlSettings


def test_defaults():
    s = Settings()
    assert s.mqtt.host == "host.docker.internal"
    assert s.mqtt.port == 1883
    assert s.api.port == 8100
    assert s.crml.log_level == "INFO"


def test_env_override(monkeypatch):
    monkeypatch.setenv("MQTT__HOST", "localhost")
    monkeypatch.setenv("API__PORT", "9000")
    s = Settings()
    assert s.mqtt.host == "localhost"
    assert s.api.port == 9000


def test_load_settings_from_yaml(tmp_path):
    from crml.config.settings import load_settings
    config = tmp_path / "config.yaml"
    config.write_text("mqtt:\n  host: testhost\n  port: 1884\n")
    s = load_settings(config)
    assert s.mqtt.host == "testhost"
    assert s.mqtt.port == 1884


def test_load_settings_env_beats_yaml(tmp_path, monkeypatch):
    from crml.config.settings import load_settings
    monkeypatch.setenv("MQTT__HOST", "envhost")
    config = tmp_path / "config.yaml"
    config.write_text("mqtt:\n  host: yamlhost\n")
    s = load_settings(config)
    assert s.mqtt.host == "envhost"


def test_load_settings_no_file():
    from crml.config.settings import load_settings
    s = load_settings(Path("nonexistent.yaml"))
    assert isinstance(s, Settings)
