"""
Unified Master Training Dataset Builder for Ornàment Qwen Coder.
Combines:
1. Design Theory & Aesthetic Craft pairs (Typographic scales, 60-30-10, 8pt grid, archetypes)
2. Semantic HTML5 & Modern Bento-Grid Components
3. Next-Gen Modern CSS (Container Queries, fluid clamp(), Subgrid, CSS variables)
4. Full Portfolio Archetypes (Developer, Designer, Founder, Studio)
5. Agentic Minimal Change Policy Bug Diagnosis Trajectories

Outputs ChatML-formatted JSONL datasets:
- ai-website-engineer-model/datasets/ornament_master_train.jsonl
- ai-website-engineer-model/datasets/ornament_master_val.jsonl
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Any

from ornament.training_data.generators.design_theory_generator import DesignTheoryGenerator

SYSTEM_PROMPT = (
    "You are Ornàment AI, an autonomous world-class website engineer and design theorist. "
    "You build production-grade, accessible, responsive websites with ultra-premium aesthetics "
    "(Swiss design, dark luxury, bento grids, tactile micro-interactions). "
    "You adhere strictly to the 60-30-10 color rule, 8-point spatial harmonics, WCAG AAA accessibility, "
    "and Ornàment's Minimal Change Policy for surgical bug repairs."
)

def build_unified_dataset():
    base_dir = Path(__file__).resolve().parent.parent.parent
    output_dir = base_dir / "ai-website-engineer-model" / "datasets"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=== Building Ornàment Unified Master Training Dataset ===")
    
    samples: List[Dict[str, Any]] = []

    # 1. Generate Design Theory & Aesthetic Craft Examples
    print("[*] Generating Design Theory & Aesthetic Craft pairs...")
    theory_examples = DesignTheoryGenerator.generate(target_count=120)
    for t in theory_examples:
        samples.append({
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": t["instruction"]},
                {"role": "assistant", "content": t["output"]}
            ],
            "category": "design_theory",
            "source": "design_theory_generator"
        })
    print(f"    Added {len(theory_examples)} Design Theory pairs.")

    # 2. Ingest Validated HTML Components
    html_file = base_dir / "ornament" / "training_data" / "datasets" / "html_train.jsonl"
    if html_file.exists():
        print(f"[*] Ingesting validated HTML components from {html_file.name}...")
        count = 0
        with open(html_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                d = json.loads(line)
                user_msg = d.get("instruction") or f"Build a modern {d.get('metadata', {}).get('category', 'web')} component."
                samples.append({
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_msg},
                        {"role": "assistant", "content": d.get("output", "")}
                    ],
                    "category": "html_components",
                    "source": "html_train"
                })
                count += 1
        print(f"    Added {count} HTML component examples.")

    # 3. Ingest Portfolio Architectures
    port_file = base_dir / "ornament" / "training_data" / "datasets" / "portfolio_train.jsonl"
    if port_file.exists():
        print(f"[*] Ingesting portfolio architectures from {port_file.name}...")
        count = 0
        with open(port_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                d = json.loads(line)
                samples.append({
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": d.get("instruction", "Build a production portfolio website.")},
                        {"role": "assistant", "content": d.get("output", "")}
                    ],
                    "category": "portfolio",
                    "source": "portfolio_train"
                })
                count += 1
        print(f"    Added {count} portfolio architecture examples.")

    # 4. Ingest Curated Minimal Change Bug Trajectories
    dbg_file = base_dir / "ornament" / "training_data" / "datasets" / "debugging_train.jsonl"
    if dbg_file.exists():
        print(f"[*] Ingesting Minimal Change Policy debugging trajectories from {dbg_file.name}...")
        dbg_samples = []
        with open(dbg_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                d = json.loads(line)
                # Format into diagnosis + minimal diff
                user_msg = (
                    f"Diagnose and fix the bug in this code according to Ornàment's Minimal Change Policy.\n\n"
                    f"Context:\n{d.get('instruction', '')}\n\n"
                    f"Code with issue:\n```html\n{d.get('input', '')}\n```"
                )
                dbg_samples.append({
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_msg},
                        {"role": "assistant", "content": d.get("output", "")}
                    ],
                    "category": "debugging",
                    "source": "debugging_train"
                })
        # Take a balanced slice of high-signal debugging cases
        selected_dbg = dbg_samples[:350]
        samples.extend(selected_dbg)
        print(f"    Added {len(selected_dbg)} curated debugging trajectory examples.")

    # 5. Shuffle and Partition (90% Train, 10% Validation)
    rng = random.Random(1337)
    rng.shuffle(samples)

    total_count = len(samples)
    val_count = max(10, int(total_count * 0.10))
    train_count = total_count - val_count

    train_data = samples[:train_count]
    val_data = samples[train_count:]

    train_path = output_dir / "ornament_master_train.jsonl"
    val_path = output_dir / "ornament_master_val.jsonl"

    with open(train_path, "w", encoding="utf-8") as f:
        for s in train_data:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    with open(val_path, "w", encoding="utf-8") as f:
        for s in val_data:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    print("\n=========================================================")
    print(f"SUCCESS: Unified Master Dataset Assembled!")
    print(f"Total Master Examples : {total_count}")
    print(f"  - Train Partition   : {len(train_data)} samples -> {train_path}")
    print(f"  - Val Partition     : {len(val_data)} samples -> {val_path}")
    print(f"Dataset format        : ChatML Standard (<|im_start|>system...user...assistant)")
    print("=========================================================\n")

if __name__ == "__main__":
    build_unified_dataset()
