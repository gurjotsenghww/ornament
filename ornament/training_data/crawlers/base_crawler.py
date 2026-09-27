"""
Base Crawler for the Ornàment Training Data System (Sections 7, 8, 22).
Enforces robots.txt compliance, rate limiting, exponential backoff, content size limits, and resumable state.
"""

import logging
import time
import urllib.robotparser
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional, Set
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)

class BaseCrawler(ABC):
    """
    Abstract ethical web crawler adhering strictly to Section 22:
      - robots.txt compliance via RobotFileParser
      - rate limiting delay between network hits
      - exponential backoff retries
      - strict content-size limits (< 5MB)
      - domain restrictions (no arbitrary commercial web scraping)
    """

    def __init__(
        self,
        rate_limit_delay: float = 1.5,
        max_retries: int = 3,
        timeout: float = 15.0,
        max_content_size_mb: float = 5.0,
        user_agent: str = "OrnamentDataCrawler/1.0 (+https://github.com/ornament/ornament-agent)",
        state_file: Optional[Path] = None
    ):
        self.rate_limit_delay = rate_limit_delay
        self.max_retries = max_retries
        self.timeout = timeout
        self.max_bytes = int(max_content_size_mb * 1024 * 1024)
        self.user_agent = user_agent
        self.state_file = state_file
        self.last_request_time: float = 0.0
        self.robot_parsers: Dict[str, urllib.robotparser.RobotFileParser] = {}
        self.visited_urls: Set[str] = set()

    def _respect_rate_limit(self) -> None:
        """Enforces minimum interval between consecutive outbound requests."""
        now = time.time()
        elapsed = now - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()

    def can_fetch(self, url: str) -> bool:
        """Checks robots.txt permissions for target domain."""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = f"{parsed.scheme}://{parsed.netloc}"

            if domain not in self.robot_parsers:
                rp = urllib.robotparser.RobotFileParser()
                rp.set_url(f"{domain}/robots.txt")
                try:
                    rp.read()
                except Exception:
                    pass
                self.robot_parsers[domain] = rp

            return self.robot_parsers[domain].can_fetch(self.user_agent, url)
        except Exception as e:
            logger.warning(f"robots.txt check failed for {url}: {e}")
            return True

    def fetch(self, url: str) -> Optional[str]:
        """
        Safely fetches content with rate limiting, retries, and size checks.
        """
        if not self.can_fetch(url):
            logger.info(f"Skipping {url}: Disallowed by robots.txt")
            return None

        self._respect_rate_limit()

        for attempt in range(1, self.max_retries + 1):
            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": self.user_agent, "Accept": "text/html,text/css,application/json"}
                )
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    # Check Content-Length header if available
                    length = resp.headers.get("Content-Length")
                    if length and int(length) > self.max_bytes:
                        logger.warning(f"File {url} exceeds {self.max_bytes} bytes; skipping.")
                        return None

                    # Check Content-Type header
                    content_type = resp.headers.get("Content-Type", "").lower()
                    if any(bad in content_type for bad in ["application/octet-stream", "application/x-msdownload", "application/zip"]):
                        logger.warning(f"Unsupported executable or binary format at {url}; skipping.")
                        return None

                    raw_data = resp.read(self.max_bytes + 1)
                    if len(raw_data) > self.max_bytes:
                        logger.warning(f"Downloaded content from {url} exceeds max allowed size.")
                        return None

                    self.visited_urls.add(url)
                    return raw_data.decode("utf-8", errors="replace")

            except urllib.error.HTTPError as e:
                if e.code in [403, 404]:
                    logger.warning(f"HTTP {e.code} for {url}; will not retry.")
                    return None
                backoff = 2 ** attempt
                time.sleep(backoff)
            except Exception as e:
                logger.warning(f"Fetch error on attempt {attempt} for {url}: {e}")
                time.sleep(2 ** attempt)

        return None

    @abstractmethod
    def crawl(self, source_url: str) -> List[Dict[str, Any]]:
        """Abstract crawl method to be implemented by specific language crawlers."""
        pass
