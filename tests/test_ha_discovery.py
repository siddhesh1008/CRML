import json
from crml.ha.discovery import discovery_payloads, state_payload, available_topic


def test_discovery_payloads_count():
    payloads = discovery_payloads("rover")
    assert len(payloads) == 5  # battery, state, pos_x, pos_y, heading


def test_discovery_topics_format():
    payloads = discovery_payloads("rover")
    for topic, _ in payloads:
        assert topic.startswith("homeassistant/sensor/crml_rover_")
        assert topic.endswith("/config")


def test_discovery_payload_valid_json():
    payloads = discovery_payloads("rover")
    for _, payload in payloads:
        data = json.loads(payload)
        assert "state_topic" in data
        assert "unique_id" in data
        assert "device" in data


def test_discovery_device_identity():
    payloads = discovery_payloads("rover")
    _, payload = payloads[0]
    data = json.loads(payload)
    assert data["device"]["identifiers"] == ["crml_rover"]
    assert "CRML" in data["device"]["name"]


def test_state_payload_maps_fields():
    topic, payload = state_payload("rover", {
        "state": "online",
        "battery": 90,
        "position": {"x": 1.5, "y": 2.0, "heading": 45.0},
    })
    assert topic == "crml/rover/state"
    data = json.loads(payload)
    assert data["battery"] == 90
    assert data["pos_x"] == 1.5
    assert data["pos_y"] == 2.0
    assert data["heading"] == 45.0
    assert data["state"] == "online"


def test_state_payload_handles_missing_fields():
    topic, payload = state_payload("rover", {"state": "idle"})
    data = json.loads(payload)
    assert data["battery"] is None
    assert data["pos_x"] is None


def test_available_topic():
    assert available_topic("rover") == "crml/rover/available"
