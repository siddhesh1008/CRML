import json
from pathlib import Path
from loguru import logger
from crml.registry.model import ModelEntry


class ModelRegistry:
    def __init__(self, models_dir: Path):
        self._dir = models_dir
        self._manifest = models_dir / "registry.json"
        self._entries: dict[str, ModelEntry] = {}
        self._loaded: dict[str, object] = {}

    def start(self) -> None:
        self._dir.mkdir(parents=True, exist_ok=True)
        if self._manifest.exists():
            with open(self._manifest) as f:
                data = json.load(f)
            for item in data.get("models", []):
                entry = ModelEntry.from_dict(item)
                self._entries[self._key(entry.name, entry.version)] = entry
            logger.info("Registry loaded {} model(s)", len(self._entries))
        else:
            self._save()
            logger.info("Registry initialised (empty)")

    def register(self, name: str, version: str, task: str, path: str) -> ModelEntry:
        entry = ModelEntry(name=name, version=version, task=task, path=path)
        self._entries[self._key(name, version)] = entry
        self._save()
        logger.info("Registered model '{}' v{} ({})", name, version, task)
        return entry

    def get(self, name: str, version: str = "latest") -> ModelEntry | None:
        if version == "latest":
            matches = [e for e in self._entries.values() if e.name == name]
            return sorted(matches, key=lambda e: e.created_at)[-1] if matches else None
        return self._entries.get(self._key(name, version))

    def list(self) -> list[ModelEntry]:
        return list(self._entries.values())

    def load(self, name: str, version: str = "latest") -> object | None:
        entry = self.get(name, version)
        if not entry:
            return None
        key = self._key(entry.name, entry.version)
        if key not in self._loaded:
            model_path = Path(entry.path)
            if not model_path.exists():
                logger.warning("Model file not found: {}", entry.path)
                return None
            # PyTorch / framework loading will be added here when models exist
            self._loaded[key] = {"path": entry.path, "task": entry.task}
            logger.info("Loaded model '{}' v{}", entry.name, entry.version)
        return self._loaded[key]

    def _key(self, name: str, version: str) -> str:
        return f"{name}:{version}"

    def _save(self) -> None:
        with open(self._manifest, "w") as f:
            json.dump({"models": [e.to_dict() for e in self._entries.values()]}, f, indent=2)
