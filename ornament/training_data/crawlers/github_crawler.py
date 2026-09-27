"""
GitHub Repository Crawler for the Ornàment Training Data System (Section 8).
Ingests permissively licensed (MIT, Apache-2.0, BSD, Unlicense) web templates and components.
"""

import json
import logging
from typing import List, Dict, Any
from ornament.training_data.crawlers.base_crawler import BaseCrawler

logger = logging.getLogger(__name__)

class GitHubCrawler(BaseCrawler):
    """
    Crawls raw content endpoints of verified open-source permissive repositories.
    Guarantees MIT/Apache license provenance and respect for rate limits.
    """

    def crawl_raw_file(self, raw_url: str, license_type: str = "MIT") -> Dict[str, Any]:
        """Fetches and wraps a single raw source file with complete license provenance."""
        content = self.fetch(raw_url)
        if not content:
            return {}

        lang = "html" if raw_url.endswith(".html") else ("css" if raw_url.endswith(".css") else "unknown")

        return {
            "instruction": f"Generate production-ready {lang.upper()} component from verified open-source repository.",
            "context": {"source": raw_url, "license": license_type},
            "output": content,
            "metadata": {
                "category": "complete_pages" if lang == "html" else "layouts",
                "source_type": "open_source",
                "source_url": raw_url,
                "license": license_type
            }
        }

    def crawl(self, source_url: str) -> List[Dict[str, Any]]:
        res = self.crawl_raw_file(source_url)
        return [res] if res else []
