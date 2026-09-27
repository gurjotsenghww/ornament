"""Configuration for training data pipeline."""
from dataclasses import dataclass, field
from typing import List

@dataclass
class TrainingDataConfig:
    target_html_examples: int = 10000
    target_css_examples: int = 10000
    html_categories: List[str] = field(default_factory=lambda: ["fundamentals", "semantic", "navigation", "headers", "heroes", "sections", "cards", "forms", "buttons", "tables", "pricing", "testimonials", "portfolios", "projects", "contact", "footers", "dashboards", "ecommerce", "accessibility", "complete_pages"])
    css_categories: List[str] = field(default_factory=lambda: ["fundamentals", "selectors", "typography", "colors", "spacing", "flexbox", "grid", "positioning", "responsive", "animations", "transitions", "hover", "cards", "buttons", "navigation", "layouts", "themes", "dark_mode", "modern_css", "complete_pages"])
    portfolio_styles: List[str] = field(default_factory=lambda: ["minimal", "modern", "premium", "luxury", "dark", "light", "futuristic", "editorial", "brutalist", "creative"])
    source_priority: List[str] = field(default_factory=lambda: ["open_source", "educational", "permissioned", "generated", "synthetic"])
    rate_limit_delay: float = 1.5
    max_retries: int = 3
    max_content_size_mb: float = 5.0
    dataset_version: str = 'v0.1'
