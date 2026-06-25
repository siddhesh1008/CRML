import json
from datetime import datetime, timezone
from pathlib import Path
from loguru import logger


class DataStore:
    def __init__(self, data_dir: Path):
        self._dir = data_dir / "raw"

    def record(self, robot_id: str, stream: str, data: dict | str) -> None:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        dest = self._dir / today / robot_id
        dest.mkdir(parents=True, exist_ok=True)

        entry = {"ts": datetime.now(timezone.utc).isoformat(), "data": data}
        with open(dest / f"{stream}.jsonl", "a") as f:
            f.write(json.dumps(entry) + "\n")

    def stats(self) -> dict:
        result: dict[str, dict[str, int]] = {}
        if not self._dir.exists():
            return result
        for robot_dir in self._dir.rglob("*"):
            if robot_dir.is_file() and robot_dir.suffix == ".jsonl":
                robot_id = robot_dir.parent.name
                stream = robot_dir.stem
                count = sum(1 for _ in open(robot_dir))
                result.setdefault(robot_id, {})[stream] = count
        return result
