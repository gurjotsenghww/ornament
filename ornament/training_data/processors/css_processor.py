"""
CSS Processor for the Ornàment Training Data System (Section 10).
Extracts selectors, variables, media queries, animations, and normalizes stylesheet declarations.
"""

import re
from typing import Dict, Any, List

class CssProcessor:
    """Cleans, normalizes, and extracts features from CSS stylesheets."""

    @classmethod
    def clean_css(cls, css_content: str) -> str:
        """
        Normalizes indentation, collapses empty rulesets, and standardizes spacing.
        """
        text = css_content.strip()

        # Remove empty rulesets: selector { }
        text = re.sub(r"[^{}]+\{\s*\}", "", text)

        # Standardize multiple consecutive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    @classmethod
    def extract_features(cls, css_content: str) -> Dict[str, Any]:
        """
        Extracts key CSS features: variables (--*), keyframe animations, media queries.
        """
        variables = re.findall(r"(--[a-zA-Z0-9_\-]+)\s*:", css_content)
        keyframes = re.findall(r"@keyframes\s+([a-zA-Z0-9_\-]+)", css_content)
        media_queries = re.findall(r"@media\s*([^{]+)", css_content)
        has_grid = "display: grid" in css_content or "display:grid" in css_content
        has_flex = "display: flex" in css_content or "display:flex" in css_content

        return {
            "custom_properties": list(set(variables)),
            "keyframes": list(set(keyframes)),
            "media_queries": [mq.strip() for mq in media_queries],
            "uses_css_grid": has_grid,
            "uses_flexbox": has_flex
        }