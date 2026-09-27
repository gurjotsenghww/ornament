"""
Multi-Level Deduplication Engine for the Ornàment Training Data System (Section 16).
Implements exact SHA-256 hash, normalized hash, and structural similarity detection.
"""

import hashlib
import json
import logging
import re
from pathlib import Path
from typing import Dict, Tuple, Optional, Set

logger = logging.getLogger(__name__)

class Deduplicator:
    """
    Multi-level deduplicator enforcing dataset diversity.
    Levels:
      1. Exact content SHA-256 hash.
      2. Normalized hash (comments removed, whitespace compressed, lowercase).
      3. Structural tag/rule sequence hash.
    """

    def __init__(self, index_file: Optional[Path] = None):
        self.index_file = index_file
        self.exact_hashes: Dict[str, str] = {}       # hash -> example_id
        self.normalized_hashes: Dict[str, str] = {}  # norm_hash -> example_id
        self.structural_hashes: Dict[str, str] = {}  # struct_hash -> example_id
        self.duplicate_count: int = 0
        if self.index_file and self.index_file.exists():
            self.load_index()

    @staticmethod
    def compute_exact_hash(content: str) -> str:
        """Compute SHA-256 of exact content bytes."""
        return hashlib.sha256(content.strip().encode("utf-8")).hexdigest()

    @staticmethod
    def compute_normalized_hash(content: str, lang: str = "html") -> str:
        """
        Compute SHA-256 of normalized content:
        Strips HTML/CSS comments, collapses inter-tag whitespace, and converts to lowercase.
        """
        text = content
        if lang.lower() == "html":
            # Remove HTML comments
            text = re.sub(r"<!--[\s\S]*?-->", "", text)
            # Normalize whitespace between tags: >  < -> ><
            text = re.sub(r">\s+<", "><", text)
        elif lang.lower() == "css":
            # Remove CSS comments
            text = re.sub(r"/\*[\s\S]*?\*/", "", text)

        # Collapse whitespace and convert to lowercase
        text = re.sub(r"\s+", " ", text).strip().lower()
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    @staticmethod
    def compute_structural_hash(content: str, lang: str = "html") -> str:
        """
        Compute structural similarity hash:
        Extracts structural tokens (tag names for HTML, selector chains for CSS).
        """
        if lang.lower() == "html":
            # Extract sequence of HTML tag names
            tags = re.findall(r"<\s*([a-zA-Z0-9\-]+)(?:\s|>)", content)
            struct_str = ">".join(t.lower() for t in tags)
        elif lang.lower() == "css":
            # Extract sequence of selector blocks
            selectors = re.findall(r"([^{]+)\{", content)
            cleaned = [re.sub(r"\s+", "", s.strip().lower()) for s in selectors]
            struct_str = ";".join(cleaned)
        else:
            struct_str = content[:100]

        return hashlib.sha256(struct_str.encode("utf-8")).hexdigest()

    def check_duplicate(self, content: str, lang: str = "html") -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Checks if content matches an existing sample at any deduplication level.
        Returns: (is_duplicate, match_type, matched_id)
        """
        exact_h = self.compute_exact_hash(content)
        if exact_h in self.exact_hashes:
            return True, "exact", self.exact_hashes[exact_h]

        norm_h = self.compute_normalized_hash(content, lang)
        if norm_h in self.normalized_hashes:
            return True, "normalized", self.normalized_hashes[norm_h]

        # Structural duplicate is flagged for short snippets with identical tag skeleton
        struct_h = self.compute_structural_hash(content, lang)
        if struct_h in self.structural_hashes and len(content.strip()) < 80:
            return True, "structural", self.structural_hashes[struct_h]

        return False, None, None

    def register(self, content: str, example_id: str, lang: str = "html") -> None:
        """Register a verified unique example into the hash registry."""
        exact_h = self.compute_exact_hash(content)
        norm_h = self.compute_normalized_hash(content, lang)
        struct_h = self.compute_structural_hash(content, lang)

        self.exact_hashes[exact_h] = example_id
        self.normalized_hashes[norm_h] = example_id
        self.structural_hashes[struct_h] = example_id

    def save_index(self) -> None:
        """Persist index to disk."""
        if not self.index_file:
            return
        self.index_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "exact_hashes": self.exact_hashes,
            "normalized_hashes": self.normalized_hashes,
            "structural_hashes": self.structural_hashes,
            "duplicate_count": self.duplicate_count
        }
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_index(self) -> None:
        """Load persisted index from disk."""
        if not self.index_file or not self.index_file.exists():
            return
        try:
            with open(self.index_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.exact_hashes = data.get("exact_hashes", {})
            self.normalized_hashes = data.get("normalized_hashes", {})
            self.structural_hashes = data.get("structural_hashes", {})
            self.duplicate_count = data.get("duplicate_count", 0)
        except Exception as e:
            logger.warning(f"Could not load dedup index from {self.index_file}: {e}")
