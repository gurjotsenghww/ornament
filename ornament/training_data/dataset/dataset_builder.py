"""
Dataset Builder for the Ornàment Training Data System (Sections 13, 14, 26).
Compiles validated examples from codes/ into normalized, split JSONL datasets:
  - html_train.jsonl, html_validation.jsonl, html_test.jsonl
  - css_train.jsonl, css_validation.jsonl, css_test.jsonl
  - portfolio_train.jsonl
  - debugging_train.jsonl
Enforces 80 / 10 / 10 isolation of test partitions.
"""

import json
import logging
import random
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class DatasetBuilder:
    """
    Transforms validated codes/ into instruction-tuning JSONL datasets
    with strict train/validation/test split isolation.
    """

    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.datasets_dir = self.base_dir / "datasets"
        self.datasets_dir.mkdir(parents=True, exist_ok=True)

    def _collect_examples(self, subpath: Path, code_file: str) -> List[Dict[str, Any]]:
        """Scans a directory for example folders containing code and metadata.json."""
        examples = []
        if not subpath.exists():
            return examples

        for d in sorted(subpath.iterdir()):
            if d.is_dir() and d.name.startswith("example_"):
                meta_file = d / "metadata.json"
                code_path = d / code_file

                if meta_file.exists() and code_path.exists():
                    try:
                        meta = json.loads(meta_file.read_text(encoding="utf-8"))
                        code = code_path.read_text(encoding="utf-8")
                        examples.append({
                            "id": meta.get("id", d.name),
                            "instruction": meta.get("description", f"Create {meta.get('category')} {meta.get('language')}"),
                            "context": {
                                "framework": meta.get("framework", "HTML/CSS"),
                                "requirements": meta.get("tags", []),
                                "category": meta.get("category", "general")
                            },
                            "input": "",
                            "output": code,
                            "metadata": {
                                "category": meta.get("category"),
                                "difficulty": meta.get("difficulty", "medium"),
                                "quality": meta.get("quality", {}).get("overall", 1.0)
                            }
                        })
                    except Exception as e:
                        logger.warning(f"Failed parsing example at {d}: {e}")

        return examples

    def _split_and_write(self, examples: List[Dict[str, Any]], prefix: str, train_ratio=0.8, val_ratio=0.1) -> Dict[str, int]:
        """Splits examples into train, validation, and test sets and writes JSONL."""
        if not examples:
            return {"train": 0, "validation": 0, "test": 0}

        # Deterministic shuffle
        rng = random.Random(42)
        shuffled = list(examples)
        rng.shuffle(shuffled)

        n = len(shuffled)
        if n == 1:
            train_set = shuffled
            val_set = []
            test_set = []
        elif n == 2:
            train_set = [shuffled[0]]
            val_set = [shuffled[1]]
            test_set = []
        else:
            val_count = max(1, int(n * val_ratio))
            test_count = max(1, int(n * (1.0 - train_ratio - val_ratio)))
            train_count = n - val_count - test_count
            if train_count < 1:
                train_count = 1
                if val_count > 1:
                    val_count -= 1
                elif test_count > 1:
                    test_count -= 1

            train_set = shuffled[:train_count]
            val_set = shuffled[train_count:train_count + val_count]
            test_set = shuffled[train_count + val_count:]

        # Write JSONL files
        def _write_jsonl(filepath: Path, items: List[Dict[str, Any]]):
            with open(filepath, "w", encoding="utf-8") as f:
                for item in items:
                    f.write(json.dumps(item) + "\n")

        _write_jsonl(self.datasets_dir / f"{prefix}_train.jsonl", train_set)
        _write_jsonl(self.datasets_dir / f"{prefix}_validation.jsonl", val_set)
        _write_jsonl(self.datasets_dir / f"{prefix}_test.jsonl", test_set)

        return {
            "train": len(train_set),
            "validation": len(val_set),
            "test": len(test_set)
        }

    def build(self, output_version: str = "dataset-v0.1") -> Dict[str, Any]:
        """
        Builds all JSONL datasets from validated codes and debugging cases.
        """
        # 1. HTML datasets
        html_examples = self._collect_examples(self.base_dir / "codes" / "html", "code.html")
        html_splits = self._split_and_write(html_examples, "html")

        # 2. CSS datasets
        css_examples = self._collect_examples(self.base_dir / "codes" / "css", "code.css")
        css_splits = self._split_and_write(css_examples, "css")

        # 3. Portfolio complete-page examples
        portfolio_examples = [ex for ex in html_examples if ex["metadata"].get("category") in ["portfolios", "complete_pages"]]
        self._split_and_write(portfolio_examples, "portfolio")

        # 4. Debugging trajectories
        debug_dir = self.base_dir / "debugging"
        debug_examples = []
        if debug_dir.exists():
            for d in sorted(debug_dir.iterdir()):
                if d.is_dir() and d.name.startswith("example_"):
                    bf = d / "bug_case.json"
                    mf = d / "metadata.json"
                    if bf.exists() and mf.exists():
                        try:
                            case = json.loads(bf.read_text(encoding="utf-8"))
                            meta = json.loads(mf.read_text(encoding="utf-8"))
                            debug_examples.append({
                                "id": meta.get("id", d.name),
                                "instruction": case.get("instruction", "Diagnose and fix web bug"),
                                "context": case.get("context", {}),
                                "input": f"Problem: {case.get('metadata', {}).get('problem', '')}\nCode:\n{case.get('metadata', {}).get('code_before', '')}",
                                "output": case.get("output", ""),
                                "metadata": meta
                            })
                        except Exception as e:
                            logger.warning(f"Failed parsing debug case at {d}: {e}")

        debug_splits = self._split_and_write(debug_examples, "debugging")

        summary = {
            "dataset_version": output_version,
            "datasets_created": {
                "html": html_splits,
                "css": css_splits,
                "portfolio": len(portfolio_examples),
                "debugging": debug_splits
            }
        }

        logger.info(f"Dataset build complete: {summary}")
        return summary
