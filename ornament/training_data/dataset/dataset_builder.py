"""Dataset builder."""
import json
from pathlib import Path

class DatasetBuilder:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def build(self, version: str):
        datasets_dir = self.data_dir / "datasets"
        datasets_dir.mkdir(exist_ok=True)
        # Just create empty JSONL for now
        for f in ["html_train.jsonl", "html_validation.jsonl", "html_test.jsonl", 
                  "css_train.jsonl", "css_validation.jsonl", "css_test.jsonl", 
                  "portfolio_train.jsonl", "debugging_train.jsonl"]:
            (datasets_dir / f).touch()
