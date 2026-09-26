import math
import re
from typing import List, Dict, Any, Tuple
from pathlib import Path

class LocalVectorStore:
    """
    Lightweight, model-independent local knowledge retrieval engine (Section 20).
    Indexes curated engineering snippets and retrieves targeted context using TF-IDF / BM25 ranking.
    Runs locally on any hardware with zero external cloud dependencies.
    """

    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.doc_freq: Dict[str, int] = {}
        self.total_docs: int = 0

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    def add_document(self, doc_id: str, title: str, category: str, content: str):
        tokens = self._tokenize(content + " " + title + " " + category)
        unique_tokens = set(tokens)

        doc = {
            "id": doc_id,
            "title": title,
            "category": category,
            "content": content,
            "tokens": tokens,
            "term_freq": {}
        }

        # Calculate term frequency
        total_tokens = len(tokens) or 1
        for t in tokens:
            doc["term_freq"][t] = doc["term_freq"].get(t, 0) + (1.0 / total_tokens)

        self.documents.append(doc)
        self.total_docs += 1

        for t in unique_tokens:
            self.doc_freq[t] = self.doc_freq.get(t, 0) + 1

    def search(self, query: str, top_k: int = 3, category: str = None) -> List[Dict[str, Any]]:
        if not self.documents:
            return []

        q_tokens = self._tokenize(query)
        scores: List[Tuple[float, Dict[str, Any]]] = []

        for doc in self.documents:
            if category and doc["category"].lower() != category.lower():
                continue

            score = 0.0
            for qt in q_tokens:
                if qt in doc["term_freq"]:
                    tf = doc["term_freq"][qt]
                    idf = math.log((self.total_docs + 1) / (self.doc_freq.get(qt, 0) + 1)) + 1.0
                    score += tf * idf

            if score > 0:
                scores.append((score, doc))

        # Sort descending by score
        scores.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scores[:top_k]]

    def load_built_in_knowledge(self):
        """Loads curated web engineering best practices (Section 20)."""
        kb_items = [
            {
                "id": "nextjs_routing_01",
                "title": "Next.js 14 App Router Dynamic & Static Links",
                "category": "Next.js",
                "content": "In Next.js App Router, routes match folder names under app/. For example, app/contact/page.tsx produces '/contact'. Links must use next/link with exact href matches: <Link href='/contact'>. Typos like '/contact-us' when the folder is 'contact' cause 404 client and server errors."
            },
            {
                "id": "tailwind_dark_mode_01",
                "title": "Tailwind CSS Dark Mode & Visual Hierarchy",
                "category": "Tailwind",
                "content": "Premium dark themes use slate-950 or zinc-900 background with subtle borders (border-zinc-800) and zinc-100 typography. Ensure primary buttons have distinct contrast with accent backgrounds (e.g. bg-white text-zinc-900 or bg-indigo-600 text-white)."
            },
            {
                "id": "a11y_navigation_01",
                "title": "Accessible Navigation & Semantic Links",
                "category": "Accessibility",
                "content": "Navigation bars must be enclosed in <nav aria-label='Main Navigation'>. All interactive items must be clickable via keyboard Tab/Enter, have visible focus rings (focus:ring-2), and text contrast must meet WCAG AA standards (4.5:1 ratio)."
            },
            {
                "id": "minimal_change_debug_01",
                "title": "Minimal Change Debugging for Component Links",
                "category": "Debugging",
                "content": "When a navigation link is broken, diagnose route mappings first before regenerating components. Compare the href attribute in the offending JSX component against existing folders in app/. A single line edit in href preserves component layout and test integrity."
            },
            {
                "id": "performance_bundle_01",
                "title": "Next.js Performance & Asset Optimization",
                "category": "Web performance",
                "content": "Use next/image with priority for hero images, dynamic imports for heavy non-critical components, and avoid unoptimized full-library imports. Keep bundle sizes minimal."
            }
        ]
        for item in kb_items:
            self.add_document(item["id"], item["title"], item["category"], item["content"])

default_vector_store = LocalVectorStore()
default_vector_store.load_built_in_knowledge()
