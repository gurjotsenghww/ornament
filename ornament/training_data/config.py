"""
Configuration module for the Ornàment Training Data System.
Defines paths, categories, quality thresholds, crawling safety constraints, and dataset settings.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict

@dataclass
class TrainingDataConfig:
    """Master configuration for the training data pipeline."""

    # Targets
    target_html_examples: int = 15000
    target_css_examples: int = 15000
    target_debugging_examples: int = 2000
    target_paired_examples: int = 3000

    # Base Directories
    base_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parent)
    
    @property
    def raw_dir(self) -> Path:
        return self.base_dir / "raw"

    @property
    def processed_dir(self) -> Path:
        return self.base_dir / "processed"

    @property
    def validated_dir(self) -> Path:
        return self.base_dir / "validated"

    @property
    def rejected_dir(self) -> Path:
        return self.base_dir / "rejected"

    @property
    def codes_dir(self) -> Path:
        return self.base_dir / "codes"

    @property
    def projects_dir(self) -> Path:
        return self.base_dir / "projects"

    @property
    def debugging_dir(self) -> Path:
        return self.base_dir / "debugging"

    @property
    def trajectories_dir(self) -> Path:
        return self.base_dir / "trajectories"

    @property
    def datasets_dir(self) -> Path:
        return self.base_dir / "datasets"

    @property
    def manifests_dir(self) -> Path:
        return self.base_dir / "manifests"

    @property
    def state_file(self) -> Path:
        return self.base_dir / "storage" / "crawl_state.json"

    @property
    def dedup_index_file(self) -> Path:
        return self.processed_dir / "dedup_index.json"

    # HTML Categories (Section 5)
    html_categories: List[str] = field(default_factory=lambda: [
        "fundamentals", "semantic", "navigation", "headers", "heroes",
        "sections", "cards", "forms", "buttons", "tables",
        "pricing", "testimonials", "portfolios", "projects", "contact",
        "footers", "dashboards", "ecommerce", "accessibility", "complete_pages"
    ])

    # CSS Categories (Section 6)
    css_categories: List[str] = field(default_factory=lambda: [
        "fundamentals", "selectors", "typography", "colors", "spacing",
        "flexbox", "grid", "positioning", "responsive", "animations",
        "transitions", "hover", "cards", "buttons", "navigation",
        "layouts", "themes", "dark_mode", "modern_css", "complete_pages"
    ])

    # Portfolio Domains & Styles (Section 18)
    portfolio_domains: List[str] = field(default_factory=lambda: [
        "developer", "designer", "founder", "photographer",
        "creative", "product_manager", "three_d", "agency"
    ])

    portfolio_styles: List[str] = field(default_factory=lambda: [
        "minimal", "modern", "premium", "luxury", "dark",
        "light", "futuristic", "editorial", "brutalist", "creative"
    ])

    # Source Priority (Section 8)
    source_priority: List[str] = field(default_factory=lambda: [
        "open_source", "educational", "permissioned", "generated", "synthetic"
    ])

    # Crawler Safety & Rate Limiting (Section 22)
    rate_limit_delay: float = 1.5      # Seconds between HTTP requests
    max_retries: int = 3
    timeout_seconds: float = 15.0
    max_content_size_mb: float = 5.0
    user_agent: str = "OrnamentDataCrawler/1.0 (+https://github.com/ornament/ornament-agent)"
    allowed_domains: List[str] = field(default_factory=lambda: [
        "raw.githubusercontent.com",
        "github.com",
        "developer.mozilla.org",
        "w3.org"
    ])

    # Quality Thresholds (Section 17)
    min_quality_score: float = 0.50

    # Dataset Versioning (Section 24)
    dataset_version: str = "dataset-v0.1"

    # Train / Val / Test Split Ratios (Section 14)
    split_ratios: Dict[str, float] = field(default_factory=lambda: {
        "train": 0.80,
        "validation": 0.10,
        "test": 0.10
    })

    def ensure_directories(self) -> None:
        """Create all required directory paths if they do not exist."""
        for p in [
            self.raw_dir, self.processed_dir, self.validated_dir, self.rejected_dir,
            self.codes_dir / "html", self.codes_dir / "css",
            self.codes_dir / "javascript", self.codes_dir / "typescript",
            self.codes_dir / "react", self.codes_dir / "nextjs",
            self.codes_dir / "tailwind", self.codes_dir / "gsap",
            self.codes_dir / "threejs", self.codes_dir / "accessibility",
            self.codes_dir / "seo", self.codes_dir / "debugging",
            self.projects_dir / "portfolio", self.projects_dir / "ecommerce",
            self.projects_dir / "saas", self.debugging_dir, self.trajectories_dir,
            self.datasets_dir, self.manifests_dir, self.base_dir / "storage"
        ]:
            p.mkdir(parents=True, exist_ok=True)
