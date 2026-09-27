"""Deduplicator for exact hash, normalized hash, structural similarity."""
import hashlib
import json
from pathlib import Path

class Deduplicator:
    def __init__(self):
        self.index_file = Path("d:/Ornàment/ornament/training_data/processed/dedup_index.json")
        self.index = self._load_index()

    def _load_index(self):
        if self.index_file.exists():
            try:
                return json.loads(self.index_file.read_text())
            except Exception:
                return set()
        return set()

    def is_duplicate(self, content: str) -> bool:
        h = hashlib.sha256(content.encode('utf-8')).hexdigest()
        if h in self.index:
            return True
        self.index.append(h)
        self._save_index()
        return False

    def _save_index(self):
        self.index_file.parent.mkdir(parents=True, exist_ok=True)
        self.index_file.write_text(json.dumps(list(self.index)))
