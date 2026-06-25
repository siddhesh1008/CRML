import json
from loguru import logger
from crml.pipeline.store import DataStore

_store: DataStore | None = None


def set_store(store: DataStore) -> None:
    global _store
    _store = store


async def dispatch(topic: str, payload: bytes) -> None:
    parts = topic.split("/")
    try:
        data = json.loads(payload)
    except (json.JSONDecodeError, ValueError):
        data = payload.decode(errors="replace")

    # robots/{robot_id}/sensors/{sensor_type}
    if len(parts) == 4 and parts[0] == "robots" and parts[2] == "sensors":
        await _handle_sensor(parts[1], parts[3], data)

    # robots/{robot_id}/status
    elif len(parts) == 3 and parts[0] == "robots" and parts[2] == "status":
        await _handle_status(parts[1], data)

    else:
        logger.debug("Unhandled topic: {}", topic)


async def _handle_sensor(robot_id: str, sensor_type: str, data) -> None:
    logger.info("Sensor | robot={} type={} data={}", robot_id, sensor_type, data)
    if _store:
        _store.record(robot_id, f"sensors_{sensor_type}", data)


async def _handle_status(robot_id: str, data) -> None:
    logger.info("Status | robot={} data={}", robot_id, data)
    if _store:
        _store.record(robot_id, "status", data)
