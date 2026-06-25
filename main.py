import asyncio
import uvicorn
from pathlib import Path
from loguru import logger
from crml.config.settings import load_settings
from crml.core.logging import setup_logging
from crml.mqtt.client import MQTTBridge
from crml.mqtt.handlers import set_store, set_bridge
from crml.registry.registry import ModelRegistry
from crml.pipeline.store import DataStore
from crml.llm.client import OllamaClient
from crml.llm.planner import TaskPlanner
from crml.api.app import app, attach_bridge, attach_registry, attach_store, attach_planner


async def main():
    settings = load_settings(Path("config.yaml"))
    setup_logging(settings.crml.log_level, settings.crml.logs_dir)
    logger.info("CRML starting up")

    store = DataStore(settings.crml.data_dir)
    set_store(store)
    attach_store(store)

    registry = ModelRegistry(settings.crml.models_dir)
    registry.start()
    attach_registry(registry)

    ollama = OllamaClient(settings.ollama.host, settings.ollama.port, settings.ollama.model)
    if await ollama.is_available():
        logger.info("Ollama connected at {}:{} model={}", settings.ollama.host, settings.ollama.port, settings.ollama.model)
        planner = TaskPlanner(ollama)
    else:
        logger.warning("Ollama not available at {}:{} — task planning disabled", settings.ollama.host, settings.ollama.port)
        planner = None
    attach_planner(planner)

    bridge = MQTTBridge(settings.mqtt)
    set_bridge(bridge)
    attach_bridge(bridge)

    server = uvicorn.Server(uvicorn.Config(
        app,
        host=settings.api.host,
        port=settings.api.port,
        log_level="warning",
    ))

    await asyncio.gather(
        bridge.run(),
        server.serve(),
    )


if __name__ == "__main__":
    asyncio.run(main())
