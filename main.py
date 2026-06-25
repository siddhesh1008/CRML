import asyncio
import uvicorn
from pathlib import Path
from loguru import logger
from crml.config.settings import load_settings
from crml.core.logging import setup_logging
from crml.mqtt.client import MQTTBridge
from crml.registry.registry import ModelRegistry
from crml.api.app import app, attach_bridge, attach_registry


async def main():
    settings = load_settings(Path("config.yaml"))
    setup_logging(settings.crml.log_level, settings.crml.logs_dir)
    logger.info("CRML starting up")

    bridge = MQTTBridge(settings.mqtt)
    attach_bridge(bridge)

    registry = ModelRegistry(settings.crml.models_dir)
    registry.start()
    attach_registry(registry)

    server = uvicorn.Server(uvicorn.Config(
        app,
        host=settings.api.host,
        port=settings.api.port,
        log_level="warning",
    ))

    # Step 6 will add the data pipeline task here
    await asyncio.gather(
        bridge.run(),
        server.serve(),
    )


if __name__ == "__main__":
    asyncio.run(main())
