"""Example store."""
import json
from pathlib import Path

class ExampleStore:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.counts = {"html": 0, "css": 0, "debugging": 0}

    def save_example(self, type_name: str, example: dict):
        self.counts[type_name] += 1
        id_str = f"{type_name}_{self.counts[type_name]:06d}"
        target_dir = self.base_dir / "codes" / type_name / f"example_{self.counts[type_name]:06d}"
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "code.txt").write_text(example["output"], encoding="utf-8")
        (target_dir / "metadata.json").write_text(json.dumps(example["metadata"]), encoding="utf-8")
        return id_str
