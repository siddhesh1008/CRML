from pathlib import Path
from crml.config.settings import load_settings
from crml.core.logging import setup_logging
from loguru import logger


def main():
    settings = load_settings(Path("config.yaml"))
    setup_logging(settings.crml.log_level, settings.crml.logs_dir)
    logger.info("CRML v{} starting up", "0.1.0")
    logger.info("MQTT -> {}:{}", settings.mqtt.host, settings.mqtt.port)
    logger.info("API  -> {}:{}", settings.api.host, settings.api.port)

    # Steps 3–6 will wire in MQTT, API, registry, and pipeline here
    logger.info("CRML ready")

    import time
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
