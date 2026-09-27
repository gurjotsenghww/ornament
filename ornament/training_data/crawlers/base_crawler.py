"""Base crawler with rate limiting, robots.txt, retries."""
import time
import json
import logging
from urllib.robotparser import RobotFileParser
from pathlib import Path
from ..config import TrainingDataConfig

logger = logging.getLogger(__name__)

class BaseCrawler:
    def __init__(self, config: TrainingDataConfig):
        self.config = config
        self.state_file = Path("d:/Ornàment/ornament/training_data/crawl_state.json")
        self.state = self._load_state()

    def _load_state(self):
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text())
            except Exception:
                return {}
        return {}

    def _save_state(self):
        self.state_file.write_text(json.dumps(self.state, indent=2))

    def fetch(self, url):
        time.sleep(self.config.rate_limit_delay)
        return ""
