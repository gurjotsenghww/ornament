"""
HTML Processor for the Ornàment Training Data System (Section 9).
Strips analytics, tracking scripts, ad iframes, and telemetry noise. Normalizes semantic markup.
"""

import re
from typing import Dict, Any, List

TRACKER_PATTERNS = [
    r"<script[\s\S]*?(?:google-analytics|googletagmanager|gtag|facebook-pixel|hotjar|intercom|mixpanel|amplitude|segment|clarity)[\s\S]*?</script>",
    r"<script[\s\S]*?(?:fbevents|adroll|criteo|doubleclick|clarity\.ms)[\s\S]*?</script>",
    r"<noscript[\s\S]*?(?:facebook|googletagmanager)[\s\S]*?</noscript>",
    r"<iframe[\s\S]*?(?:doubleclick|googlesyndication|adnxs)[\s\S]*?</iframe>"
]

class HtmlProcessor:
    """Cleans, normalizes, and extracts production-grade HTML from raw content."""

    @classmethod
    def clean_html(cls, html_content: str) -> str:
        """
        Strips tracking scripts, cookies/analytics tags, and normalizes indentation.
        """
        text = html_content

        # Remove known tracking scripts and third-party ad iframes
        for pattern in TRACKER_PATTERNS:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)

        # Remove generic empty tracking scripts
        text = re.sub(r'<script\b[^>]*>(?:\s*//<!\[CDATA\[)?(?:\s*//\]\]>)?\s*</script>', '', text, flags=re.IGNORECASE)

        # Normalize multiple blank lines to at most two
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        return text

    @classmethod
    def extract_sections(cls, html_content: str) -> List[Dict[str, str]]:
        """
        Extracts individual component/section blocks (header, nav, section, footer, article, form).
        """
        sections = []
        tags = ["header", "nav", "main", "section", "article", "aside", "footer", "form"]
        for tag in tags:
            pattern = rf"(<{tag}\b[\s\S]*?</{tag}>)"
            matches = re.findall(pattern, html_content, flags=re.IGNORECASE)
            for m in matches:
                if len(m.strip()) > 50:
                    sections.append({
                        "tag": tag,
                        "content": cls.clean_html(m)
                    })
        return sections