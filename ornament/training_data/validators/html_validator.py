"""
HTML Validator for the Ornàment Training Data System (Section 15).
Validates syntax, tag balancing, semantic quality, and core WCAG accessibility attributes.
"""

from html.parser import HTMLParser
from typing import List, Tuple, Dict, Any, Optional

VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr"
}

SEMANTIC_LANDMARKS = {
    "header", "nav", "main", "section", "article", "footer", "aside", "figure"
}

class _HTMLStructureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack: List[str] = []
        self.errors: List[str] = []
        self.semantic_elements_found: List[str] = []
        self.a11y_issues: List[str] = []
        self.total_tags: int = 0
        self.has_text: bool = False

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]):
        self.total_tags += 1
        attr_dict = {k.lower(): (v or "") for k, v in attrs}

        if tag.lower() in SEMANTIC_LANDMARKS:
            self.semantic_elements_found.append(tag.lower())

        # Accessibility checks
        if tag.lower() == "img":
            if "alt" not in attr_dict:
                self.a11y_issues.append("<img> element missing 'alt' attribute")

        if tag.lower() == "input":
            input_type = attr_dict.get("type", "text").lower()
            if input_type not in ["hidden", "submit", "reset", "button"]:
                has_label = any(k in attr_dict for k in ["aria-label", "aria-labelledby", "placeholder", "id", "name"])
                if not has_label:
                    self.a11y_issues.append("<input> element lacks accessible label or placeholder")

        if tag.lower() not in VOID_TAGS:
            self.stack.append(tag.lower())

    def handle_endtag(self, tag: str):
        tag_l = tag.lower()
        if tag_l in VOID_TAGS:
            return

        if not self.stack:
            self.errors.append(f"Unexpected closing tag </{tag_l}> with no matching open tag")
            return

        # Find matching tag in stack
        if self.stack[-1] == tag_l:
            self.stack.pop()
        else:
            # Check if tag is in stack earlier (unclosed inner tags)
            if tag_l in self.stack:
                while self.stack and self.stack[-1] != tag_l:
                    unclosed = self.stack.pop()
                    self.errors.append(f"Unclosed tag <{unclosed}> before closing </{tag_l}>")
                if self.stack:
                    self.stack.pop()
            else:
                self.errors.append(f"Mismatched closing tag </{tag_l}>; expected </{self.stack[-1]}>")

    def handle_data(self, data: str):
        if data.strip():
            self.has_text = True

class HtmlValidator:
    """Validates HTML syntax, tag balancing, semantic quality, and accessibility."""

    @classmethod
    def validate(cls, html_content: str) -> Tuple[bool, List[str], float]:
        """
        Validates an HTML string.
        Returns:
            is_valid (bool): True if syntactically sound.
            errors (List[str]): List of syntax or accessibility violations.
            score (float): 0.0 to 1.0 quality score.
        """
        if not html_content or not html_content.strip():
            return False, ["HTML content is empty"], 0.0

        content = html_content.strip()
        parser = _HTMLStructureParser()

        try:
            parser.feed(content)
            parser.close()
        except Exception as e:
            return False, [f"HTML parsing exception: {str(e)}"], 0.1

        # Check remaining unclosed tags
        for unclosed in parser.stack:
            parser.errors.append(f"Unclosed tag <{unclosed}> at end of document")

        errors = parser.errors + parser.a11y_issues
        is_valid = len(parser.errors) == 0 and parser.total_tags > 0

        # Compute score
        score = 1.0
        if parser.errors:
            score -= min(0.6, len(parser.errors) * 0.2)
        if parser.a11y_issues:
            score -= min(0.3, len(parser.a11y_issues) * 0.1)

        # Semantic landmark bonus
        if parser.semantic_elements_found:
            score = min(1.0, score + 0.1)

        score = max(0.0, min(1.0, score))
        return is_valid, errors, round(score, 3)