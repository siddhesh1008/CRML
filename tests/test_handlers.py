import pytest
from unittest.mock import MagicMock, patch
from crml.mqtt import handlers


@pytest.fixture(autouse=True)
def reset_store():
    handlers.set_store(None)
    yield
    handlers.set_store(None)


@pytest.mark.asyncio
async def test_dispatch_sensor():
    store = MagicMock()
    handlers.set_store(store)
    await handlers.dispatch("robots/rover/sensors/camera", b'{"objects": ["chair"]}')
    store.record.assert_called_once_with("rover", "sensors_camera", {"objects": ["chair"]})


@pytest.mark.asyncio
async def test_dispatch_status():
    store = MagicMock()
    handlers.set_store(store)
    await handlers.dispatch("robots/rover/status", b'{"battery": 90}')
    store.record.assert_called_once_with("rover", "status", {"battery": 90})


@pytest.mark.asyncio
async def test_dispatch_malformed_json():
    store = MagicMock()
    handlers.set_store(store)
    await handlers.dispatch("robots/rover/status", b"not-json")
    store.record.assert_called_once_with("rover", "status", "not-json")


@pytest.mark.asyncio
async def test_dispatch_unknown_topic():
    store = MagicMock()
    handlers.set_store(store)
    await handlers.dispatch("unknown/topic", b"{}")
    store.record.assert_not_called()


@pytest.mark.asyncio
async def test_dispatch_no_store():
    # Should not raise even when store is None
    await handlers.dispatch("robots/rover/status", b'{"battery": 90}')
