"""
CSS Validator for the Ornàment Training Data System (Section 15).
Validates CSS syntax, balanced blocks, ruleset integrity, and property-value pairs.
"""

import re
from typing import List, Tuple

class CssValidator:
    """Validates CSS stylesheet syntax, balanced block braces, and declaration integrity."""

    @classmethod
    def validate(cls, css_content: str) -> Tuple[bool, List[str], float]:
        """
        Validates CSS content.
        Returns:
            is_valid (bool): True if syntactically sound.
            errors (List[str]): List of syntax errors or warnings.
            score (float): 0.0 to 1.0 quality score.
        """
        if not css_content or not css_content.strip():
            return False, ["CSS content is empty"], 0.0

        content = css_content.strip()
        errors: List[str] = []

        # 1. Balanced Braces Check
        brace_stack = []
        paren_stack = []
        in_comment = False
        i = 0
        n = len(content)

        while i < n:
            if not in_comment and content[i:i+2] == "/*":
                in_comment = True
                i += 2
                continue
            if in_comment and content[i:i+2] == "*/":
                in_comment = False
                i += 2
                continue
            if in_comment:
                i += 1
                continue

            char = content[i]
            if char == "{":
                brace_stack.append(i)
            elif char == "}":
                if not brace_stack:
                    errors.append(f"Unmatched closing brace '}}' at character index {i}")
                else:
                    brace_stack.pop()
            elif char == "(":
                paren_stack.append(i)
            elif char == ")":
                if not paren_stack:
                    errors.append(f"Unmatched closing parenthesis ')' at character index {i}")
                else:
                    paren_stack.pop()
            i += 1

        if in_comment:
            errors.append("Unclosed comment block '/* ...' at end of file")

        for b in brace_stack:
            errors.append(f"Unclosed opening brace '{{' at character index {b}")

        for p in paren_stack:
            errors.append(f"Unclosed opening parenthesis '(' at character index {p}")

        # 2. Ruleset Structure & Declarations Check
        # Strip comments for rule analysis
        clean_css = re.sub(r"/\*[\s\S]*?\*/", "", content)

        # Match rulesets: selector { declarations }
        # Exclude @media, @keyframes, @container, etc.
        blocks = re.findall(r"([^{}]+)\{([^{}]*)\}", clean_css)
        valid_rules = 0

        for selector, declarations in blocks:
            sel = selector.strip()
            # If it's an at-rule (like @keyframes fade-in) or valid selector
            if sel:
                valid_rules += 1
            else:
                errors.append("Empty selector before block '{ ... }'")

            decls = declarations.strip()
            if decls and not sel.startswith("@"):
                # Split declarations by semicolon
                items = [d.strip() for d in decls.split(";") if d.strip()]
                for item in items:
                    if ":" not in item:
                        errors.append(f"Invalid CSS declaration '{item}' missing colon in selector '{sel}'")

        is_valid = len(errors) == 0 and (valid_rules > 0 or len(clean_css.strip()) > 0)

        # Score computation
        score = 1.0
        if errors:
            score -= min(0.7, len(errors) * 0.15)
        if valid_rules == 0 and len(clean_css.strip()) > 0:
            score -= 0.3

        score = max(0.0, min(1.0, score))
        return is_valid, errors, round(score, 3)