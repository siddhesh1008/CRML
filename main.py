import asyncio
import uvicorn
from pathlib import Path
from loguru import logger
from crml.config.settings import load_settings
from crml.core.logging import setup_logging
from crml.mqtt.client import MQTTBridge
from crml.api.app import app, attach_bridge


async def main():
    settings = load_settings(Path("config.yaml"))
    setup_logging(settings.crml.log_level, settings.crml.logs_dir)
    logger.info("CRML starting up")

    bridge = MQTTBridge(settings.mqtt)
    attach_bridge(bridge)

    server = uvicorn.Server(uvicorn.Config(
        app,
        host=settings.api.host,
        port=settings.api.port,
        log_level="warning",
    ))

    # Steps 5–6 will add registry and pipeline tasks here
    await asyncio.gather(
        bridge.run(),
        server.serve(),
    )


if __name__ == "__main__":
    asyncio.run(main())
