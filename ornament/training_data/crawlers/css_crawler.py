"""
CSS Crawler for the Ornàment Training Data System (Section 7, 10).
Discovers and extracts normalized CSS declarations and design tokens.
"""

from typing import List, Dict, Any
from ornament.training_data.crawlers.base_crawler import BaseCrawler
from ornament.training_data.processors.css_processor import CssProcessor

class CssCrawler(BaseCrawler):
    """Fetches, cleans, and extracts stylesheets and rules from open repositories."""

    def crawl(self, source_url: str) -> List[Dict[str, Any]]:
        raw = self.fetch(source_url)
        if not raw:
            return []

        cleaned = CssProcessor.clean_css(raw)
        features = CssProcessor.extract_features(cleaned)

        cat = "modern_css" if features["custom_properties"] else ("animations" if features["keyframes"] else "layouts")

        return [{
            "instruction": f"Implement stylesheet rules for {cat}.",
            "context": {"framework": "CSS3", "source_url": source_url},
            "output": cleaned,
            "metadata": {
                "category": cat,
                "features": features,
                "source_type": "open_source",
                "source_url": source_url,
                "license": "Permissive / Open Education"
            }
        }]
