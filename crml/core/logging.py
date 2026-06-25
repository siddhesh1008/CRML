import sys
from pathlib import Path
from loguru import logger


def setup_logging(log_level: str = "INFO", logs_dir: Path = Path("logs")) -> None:
    logs_dir.mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(sys.stdout, level=log_level, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan> - {message}")
    logger.add(logs_dir / "crml.log", level=log_level, rotation="10 MB", retention="7 days")
