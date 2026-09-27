"""CSS generator."""
import random
from typing import List

def generate_css(count: int, categories: List[str]):
    results = []
    for i in range(count):
        cat = random.choice(categories) if categories else "flexbox"
        results.append({
            "instruction": f"Create {cat} css",
            "context": {"framework": "CSS", "requirements": []},
            "output": f".{cat}-{i} {{ display: flex; }}",
            "metadata": {"category": cat, "difficulty": "medium"}
        })
    return results
