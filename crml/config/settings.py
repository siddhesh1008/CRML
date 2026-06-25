from pathlib import Path
import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class MqttTopics(BaseModel):
    subscribe: str = "robots/#"
    publish: str = "crml/#"


class MqttSettings(BaseModel):
    host: str = "host.docker.internal"
    port: int = 1883
    client_id: str = "crml"
    topics: MqttTopics = MqttTopics()


class ApiSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8100


class CrmlSettings(BaseModel):
    log_level: str = "INFO"
    data_dir: Path = Path("data")
    models_dir: Path = Path("models")
    logs_dir: Path = Path("logs")


class Settings(BaseSettings):
    crml: CrmlSettings = CrmlSettings()
    mqtt: MqttSettings = MqttSettings()
    api: ApiSettings = ApiSettings()

    model_config = {"env_file": ".env", "env_nested_delimiter": "__"}


def load_settings(config_path: Path = Path("config.yaml")) -> Settings:
    if config_path.exists():
        with open(config_path) as f:
            data = yaml.safe_load(f)
        return Settings(**data)
    return Settings()
