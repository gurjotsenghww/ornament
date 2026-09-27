"""
HTML Crawler for the Ornàment Training Data System (Section 7, 9).
Discovers and extracts clean, accessible semantic HTML from permissioned open-source sources.
"""

from typing import List, Dict, Any
from ornament.training_data.crawlers.base_crawler import BaseCrawler
from ornament.training_data.processors.html_processor import HtmlProcessor

class HtmlCrawler(BaseCrawler):
    """Fetches and extracts semantic HTML structures from permissible repositories and documentation."""

    def crawl(self, source_url: str) -> List[Dict[str, Any]]:
        raw = self.fetch(source_url)
        if not raw:
            return []

        cleaned = HtmlProcessor.clean_html(raw)
        sections = HtmlProcessor.extract_sections(cleaned)
        results = []

        if sections:
            for s in sections:
                results.append({
                    "instruction": f"Build a clean, accessible {s['tag']} component.",
                    "context": {"framework": "HTML5", "source_url": source_url},
                    "output": s["content"],
                    "metadata": {
                        "category": s["tag"] if s["tag"] in ["header", "nav", "footer", "form"] else "sections",
                        "source_type": "open_source",
                        "source_url": source_url,
                        "license": "Permissive / Open Education"
                    }
                })
        else:
            results.append({
                "instruction": "Construct a semantic HTML layout page.",
                "context": {"framework": "HTML5", "source_url": source_url},
                "output": cleaned,
                "metadata": {
                    "category": "complete_pages",
                    "source_type": "open_source",
                    "source_url": source_url,
                    "license": "Permissive / Open Education"
                }
            })

        return results
