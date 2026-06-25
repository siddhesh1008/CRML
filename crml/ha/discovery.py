import json

DISCOVERY_PREFIX = "homeassistant"


def _config_topic(robot_id: str, sensor: str) -> str:
    return f"{DISCOVERY_PREFIX}/sensor/crml_{robot_id}_{sensor}/config"


def _state_topic(robot_id: str) -> str:
    return f"crml/{robot_id}/state"


def discovery_payloads(robot_id: str) -> list[tuple[str, str]]:
    state_topic = _state_topic(robot_id)
    base = {
        "device": {
            "identifiers": [f"crml_{robot_id}"],
            "name": f"CRML {robot_id.capitalize()}",
            "model": "CRML Robot",
            "manufacturer": "CR_Master",
        },
        "availability_topic": f"crml/{robot_id}/available",
    }

    sensors = [
        ("battery",  {"name": f"{robot_id.capitalize()} Battery",  "unit_of_measurement": "%",   "device_class": "battery",    "value_template": "{{ value_json.battery }}"}),
        ("state",    {"name": f"{robot_id.capitalize()} State",    "value_template": "{{ value_json.state }}"}),
        ("pos_x",    {"name": f"{robot_id.capitalize()} X",        "unit_of_measurement": "m",   "value_template": "{{ value_json.pos_x }}"}),
        ("pos_y",    {"name": f"{robot_id.capitalize()} Y",        "unit_of_measurement": "m",   "value_template": "{{ value_json.pos_y }}"}),
        ("heading",  {"name": f"{robot_id.capitalize()} Heading",  "unit_of_measurement": "°",   "value_template": "{{ value_json.heading }}"}),
    ]

    result = []
    for sensor, extra in sensors:
        payload = {**base, "state_topic": state_topic, "unique_id": f"crml_{robot_id}_{sensor}", **extra}
        result.append((_config_topic(robot_id, sensor), json.dumps(payload)))
    return result


def state_payload(robot_id: str, data: dict) -> tuple[str, str]:
    position = data.get("position", {})
    state = {
        "battery": data.get("battery"),
        "state":   data.get("state", "unknown"),
        "pos_x":   position.get("x"),
        "pos_y":   position.get("y"),
        "heading": position.get("heading"),
    }
    return (_state_topic(robot_id), json.dumps(state))


def available_topic(robot_id: str) -> str:
    return f"crml/{robot_id}/available"
