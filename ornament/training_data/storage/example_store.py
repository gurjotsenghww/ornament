"""
Example Store for the Ornàment Training Data System (Sections 3, 4, 14, 16, 26).
Manages persistent, resumable, deduplicated storage of training samples with full provenance.
"""

import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

from ornament.training_data.processors.deduplicator import Deduplicator
from ornament.training_data.processors.quality_scorer import QualityScorer
from ornament.training_data.processors.html_processor import HtmlProcessor
from ornament.training_data.processors.css_processor import CssProcessor

logger = logging.getLogger(__name__)

class ExampleStore:
    """
    Persistent storage engine managing the lifecycle:
      RAW -> PROCESSED -> DEDUPLICATED -> VALIDATED / REJECTED -> CODES
    Enforces stable IDs (html_000001, css_000001, etc.), provenance metadata, and state recovery.
    """

    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.state_file = self.base_dir / "storage" / "crawl_state.json"
        self.dedup_index_file = self.base_dir / "processed" / "dedup_index.json"
        self.deduplicator = Deduplicator(self.dedup_index_file)

        # Counter states
        self.counts = {
            "html": 0,
            "css": 0,
            "paired": 0,
            "debugging": 0,
            "trajectory": 0,
            "validated": 0,
            "rejected": 0,
            "duplicates": 0
        }
        self.category_counts: Dict[str, Dict[str, int]] = {
            "html": {},
            "css": {},
            "paired": {},
            "debugging": {}
        }
        self.load_state()

    def load_state(self) -> None:
        """Load state and restore counters for seamless resumability."""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.counts.update(data.get("counts", {}))
                self.category_counts.update(data.get("category_counts", {}))
                logger.info(f"Loaded store state: {self.counts}")
            except Exception as e:
                logger.warning(f"Could not load state file {self.state_file}: {e}")

    def save_state(self) -> None:
        """Persist state to disk."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "counts": self.counts,
            "category_counts": self.category_counts
        }
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        self.deduplicator.save_index()

    def save_example(
        self,
        lang: str,
        example_data: Dict[str, Any],
        source_info: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Processes, validates, deduplicates, and saves an example.
        Returns:
            (success: bool, example_id_or_error: str, rejection_reason: Optional[str])
        """
        lang = lang.lower()
        content = example_data.get("output", "")
        if not content and lang in ["html", "css"]:
            return False, "empty_content", "Code content was empty"

        # 1. Clean Content
        if lang == "html":
            content = HtmlProcessor.clean_html(content)
        elif lang == "css":
            content = CssProcessor.clean_css(content)

        # 2. Check Deduplication
        if lang in ["html", "css"]:
            is_dup, match_type, matched_id = self.deduplicator.check_duplicate(content, lang=lang)
            if is_dup:
                self.counts["duplicates"] += 1
                return False, matched_id, f"Duplicate detected ({match_type} match with {matched_id})"

        # 3. Quality Scoring & Validation
        category = example_data.get("metadata", {}).get("category", "general")
        meta = example_data.get("metadata", {})
        quality = QualityScorer.score_example(content, lang=lang, metadata=meta)

        if not quality["passed"] and lang in ["html", "css"]:
            self.counts["rejected"] += 1
            # Save to rejected/ for inspection
            rej_id = f"rejected_{self.counts['rejected']:06d}"
            rej_dir = self.base_dir / "rejected" / rej_id
            rej_dir.mkdir(parents=True, exist_ok=True)
            (rej_dir / f"code.{lang}").write_text(content, encoding="utf-8")
            (rej_dir / "rejection.json").write_text(json.dumps({
                "quality": quality,
                "metadata": meta,
                "rejected_at": datetime.now(timezone.utc).isoformat()
            }, indent=2), encoding="utf-8")
            return False, rej_id, f"Failed quality threshold (score: {quality['overall']})"

        # 4. Generate Stable ID and Directory Structure
        self.counts[lang] = self.counts.get(lang, 0) + 1
        example_num = self.counts[lang]
        example_id = f"{lang}_{example_num:06d}"

        # Determine target directory
        if lang == "html":
            target_dir = self.base_dir / "codes" / "html" / f"example_{example_num:06d}"
            code_filename = "code.html"
        elif lang == "css":
            target_dir = self.base_dir / "codes" / "css" / f"example_{example_num:06d}"
            code_filename = "code.css"
        elif lang == "debugging":
            target_dir = self.base_dir / "debugging" / f"example_{example_num:06d}"
            code_filename = "bug_case.json"
        elif lang == "paired":
            cat = meta.get("category", "portfolio")
            target_dir = self.base_dir / "projects" / cat / f"example_{example_num:06d}"
            code_filename = "index.html"
        else:
            target_dir = self.base_dir / "codes" / lang / f"example_{example_num:06d}"
            code_filename = f"code.{lang}"

        target_dir.mkdir(parents=True, exist_ok=True)

        # 5. Write Code File
        if lang == "debugging":
            (target_dir / code_filename).write_text(json.dumps(example_data, indent=2), encoding="utf-8")
        elif lang == "paired":
            (target_dir / "index.html").write_text(example_data.get("html", ""), encoding="utf-8")
            (target_dir / "styles.css").write_text(example_data.get("css", ""), encoding="utf-8")
        else:
            (target_dir / code_filename).write_text(content, encoding="utf-8")

        # 6. Write Full Metadata (Section 4)
        full_metadata = {
            "id": example_id,
            "language": lang,
            "category": category,
            "subcategory": meta.get("subcategory", meta.get("style", "general")),
            "difficulty": meta.get("difficulty", "medium"),
            "description": example_data.get("instruction", meta.get("description", f"High quality {lang} {category}")),
            "tags": meta.get("tags", [lang, category, "production-quality"]),
            "framework": meta.get("framework", "html-css-tailwind"),
            "source_type": meta.get("source_type", "open_source"),
            "license": meta.get("license", "MIT"),
            "source_url": meta.get("source_url", "https://github.com/ornament/curated-web-data"),
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "validated": True,
            "quality": quality
        }
        (target_dir / "metadata.json").write_text(json.dumps(full_metadata, indent=2), encoding="utf-8")

        # 7. Write Source Provenance
        provenance = source_info or {
            "source_type": meta.get("source_type", "open_source"),
            "license": meta.get("license", "MIT"),
            "source_url": meta.get("source_url", "https://github.com/ornament/curated-web-data"),
            "original_id": meta.get("original_id", example_id),
            "collected_at": datetime.now(timezone.utc).isoformat()
        }
        (target_dir / "source.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")

        # 8. Register in Deduplicator & Category Counts
        if lang in ["html", "css"]:
            self.deduplicator.register(content, example_id, lang=lang)

        self.counts["validated"] += 1
        lang_cat = self.category_counts.setdefault(lang, {})
        lang_cat[category] = lang_cat.get(category, 0) + 1

        # Checkpoint every 50 examples
        if self.counts["validated"] % 50 == 0:
            self.save_state()

        return True, example_id, None

    def get_stats(self) -> Dict[str, Any]:
        """Returns live statistics on collected examples, validation, and categories."""
        return {
            "counts": self.counts,
            "category_counts": self.category_counts,
            "dedup_registered_hashes": len(self.deduplicator.exact_hashes),
            "rejected_samples": self.counts["rejected"],
            "duplicate_skips": self.counts["duplicates"]
        }
