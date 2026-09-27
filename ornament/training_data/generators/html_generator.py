"""HTML generator."""
import random
from typing import List

def generate_html(count: int, categories: List[str]):
    results = []
    for i in range(count):
        cat = random.choice(categories) if categories else "heroes"
        results.append({
            "instruction": f"Create {cat} html",
            "context": {"framework": "HTML", "requirements": []},
            "output": f"<main class='{cat}'><section><h1>Hero {i}</h1></section></main>",
            "metadata": {"category": cat, "difficulty": "medium"}
        })
    return results
