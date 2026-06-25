import asyncio
from pathlib import Path
from loguru import logger
from crml.config.settings import load_settings
from crml.core.logging import setup_logging
from crml.mqtt.client import MQTTBridge


async def main():
    settings = load_settings(Path("config.yaml"))
    setup_logging(settings.crml.log_level, settings.crml.logs_dir)
    logger.info("CRML starting up")

    bridge = MQTTBridge(settings.mqtt)

    # Steps 4–6 will add more tasks here (API, registry, pipeline)
    await asyncio.gather(
        bridge.run(),
    )


if __name__ == "__main__":
    asyncio.run(main())
