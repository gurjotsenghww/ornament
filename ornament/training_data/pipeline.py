"""
Master Pipeline Orchestrator for the Ornàment Training Data System (Sections 1, 14, 26).
Coordinates the complete lifecycle:
  SOURCE -> CRAWLER / GENERATOR -> RAW -> CLEAN -> DEDUPLICATE -> VALIDATE -> QUALITY SCORE -> VALIDATED -> DATASET BUILDER -> JSONL
"""

import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

from ornament.training_data.config import TrainingDataConfig
from ornament.training_data.storage.example_store import ExampleStore
from ornament.training_data.storage.manifest_builder import ManifestBuilder
from ornament.training_data.dataset.dataset_builder import DatasetBuilder
from ornament.training_data.generators.html_generator import generate_html
from ornament.training_data.generators.css_generator import generate_css
from ornament.training_data.generators.debugging_generator import generate_debugging
from ornament.training_data.generators.paired_generator import generate_paired

logger = logging.getLogger(__name__)

class TrainingDataPipeline:
    """
    Reusable, resumable data pipeline managing collection, validation,
    and compilation of Ornàment training datasets.
    """

    def __init__(self, config: Optional[TrainingDataConfig] = None):
        self.config = config or TrainingDataConfig()
        self.config.ensure_directories()
        self.store = ExampleStore(self.config.base_dir)
        self.manifest_builder = ManifestBuilder(self.config.base_dir)
        self.dataset_builder = DatasetBuilder(self.config.base_dir)

    def collect(self, data_type: str, count: int, categories: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Executes generation and ingestion of examples into the store.
        """
        data_type = data_type.lower()
        logger.info(f"Initiating collection for {count} {data_type} examples...")

        if data_type == "html":
            examples = generate_html(count, categories or self.config.html_categories)
        elif data_type == "css":
            examples = generate_css(count, categories or self.config.css_categories)
        elif data_type == "debugging":
            examples = generate_debugging(count)
        elif data_type == "paired":
            examples = generate_paired(count)
        else:
            raise ValueError(f"Unsupported data type '{data_type}'. Use html, css, debugging, or paired.")

        saved_count = 0
        duplicates = 0
        rejected = 0

        for ex in examples:
            success, ex_id, reason = self.store.save_example(data_type, ex)
            if success:
                saved_count += 1
            elif "Duplicate" in (reason or ""):
                duplicates += 1
            else:
                rejected += 1

        self.store.save_state()

        return {
            "requested": count,
            "saved": saved_count,
            "duplicates": duplicates,
            "rejected": rejected,
            "total_validated": self.store.counts["validated"]
        }

    def build_datasets(self, version: Optional[str] = None) -> Dict[str, Any]:
        """
        Compiles stored validated examples into JSONL datasets and writes manifests.
        """
        ver = version or self.config.dataset_version
        logger.info(f"Compiling JSONL datasets for version {ver}...")

        dataset_summary = self.dataset_builder.build(ver)
        manifest_summary = self.manifest_builder.build_manifest(ver, self.store.get_stats())

        return {
            "version": ver,
            "datasets": dataset_summary,
            "manifest": manifest_summary
        }

    def get_status(self) -> Dict[str, Any]:
        """Returns comprehensive status of current pipeline storage."""
        return self.store.get_stats()
