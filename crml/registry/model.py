from dataclasses import dataclass, asdict
from datetime import datetime, timezone


@dataclass
class ModelEntry:
    name: str
    version: str
    task: str        # perception | motion | task
    path: str
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "ModelEntry":
        return ModelEntry(**data)
