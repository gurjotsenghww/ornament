"""
Quality Scorer for the Ornàment Training Data System (Section 17).
Evaluates examples across syntax, structure, complexity, uniqueness, and documentation.
"""

import re
from typing import Dict, Any, Tuple
from ornament.training_data.validators.html_validator import HtmlValidator
from ornament.training_data.validators.css_validator import CssValidator

class QualityScorer:
    """
    Computes a 5-dimension quality score (0.0 to 1.0) for every training example:
      - syntax: validator pass and cleanliness
      - structure: semantic tag depth or CSS rule completeness
      - complexity: code length and non-triviality
      - uniqueness: distinction from trivial patterns
      - documentation: presence of descriptive classes, attributes, or comments
    """

    @classmethod
    def score_example(
        cls,
        content: str,
        lang: str = "html",
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Calculates the quality breakdown and overall score for a sample.
        Returns:
            Dict containing individual dimension scores, overall score, and passed status.
        """
        metadata = metadata or {}
        lang = lang.lower()

        # 1. Syntax Score
        if lang == "html":
            is_valid, errors, syntax_score = HtmlValidator.validate(content)
        elif lang == "css":
            is_valid, errors, syntax_score = CssValidator.validate(content)
        else:
            is_valid, errors, syntax_score = True, [], 1.0

        # 2. Structure Score
        structure_score = 0.5
        if lang == "html":
            # Count semantic landmarks & structural elements
            landmarks = ["header", "nav", "main", "section", "article", "footer", "aside", "figure"]
            found = sum(1 for lm in landmarks if f"<{lm}" in content.lower())
            structure_score = min(1.0, 0.4 + (found * 0.12))
        elif lang == "css":
            # Check for media queries, root variables, flex/grid
            has_vars = "--" in content
            has_media = "@media" in content
            has_layout = "display: flex" in content or "display: grid" in content
            structure_score = 0.4 + (0.2 if has_vars else 0) + (0.2 if has_media else 0) + (0.2 if has_layout else 0)

        # 3. Complexity Score (favor non-trivial components over 2-line snippets)
        lines = [l.strip() for l in content.splitlines() if l.strip()]
        line_count = len(lines)
        if line_count < 3:
            complexity_score = 0.2
        elif line_count < 10:
            complexity_score = 0.5
        elif line_count < 40:
            complexity_score = 0.85
        else:
            complexity_score = 0.95

        # 4. Uniqueness Score (check against trivial generic patterns)
        uniqueness_score = 0.9
        trivial_patterns = ["<div>hello</div>", "<p>test</p>", "body { color: red; }", "<h1>test</h1>"]
        if any(p in content.lower() for p in trivial_patterns) and line_count < 4:
            uniqueness_score = 0.2

        # 5. Documentation Score (meaningful class names, comments, aria labels)
        doc_score = 0.5
        has_comments = "/*" in content or "<!--" in content
        has_aria = "aria-" in content or "role=" in content
        has_meaningful_classes = bool(re.search(r'class="[a-zA-Z0-9_\-\s]{10,}"', content))

        doc_score = 0.3 + (0.25 if has_comments else 0) + (0.25 if has_aria else 0) + (0.2 if has_meaningful_classes else 0)
        doc_score = min(1.0, doc_score)

        # Weighted Overall Score
        overall = (
            0.30 * syntax_score +
            0.25 * structure_score +
            0.20 * complexity_score +
            0.15 * uniqueness_score +
            0.10 * doc_score
        )
        overall = round(max(0.0, min(1.0, overall)), 3)

        quality_breakdown = {
            "syntax": round(syntax_score, 3),
            "structure": round(structure_score, 3),
            "complexity": round(complexity_score, 3),
            "uniqueness": round(uniqueness_score, 3),
            "documentation": round(doc_score, 3),
            "overall": overall,
            "passed": overall >= 0.50 and is_valid,
            "validation_errors": errors
        }

        return quality_breakdown
