#!/usr/bin/env python3
"""
Synthetic Trajectory Dataset Generator for Ornàment (Section 38).
Generates diverse engineering combinations (industry, style, layout, typography, components)
and outputs structured (task -> plan -> changes -> test -> failure -> diagnosis -> fix -> status)
trajectories for LoRA fine-tuning.
"""
import argparse
import itertools
import json
import random
from pathlib import Path
from typing import List, Dict, Any

INDUSTRIES = ["Technology", "Design", "Finance", "Healthcare", "E-commerce", "AI Infrastructure"]
PROFESSIONS = ["Senior Full Stack Engineer", "Autonomous Systems Architect", "Creative Director", "Product Designer", "Security Researcher"]
STYLES = ["dark futuristic", "minimal luxury", "editorial brutalist", "modern clean", "high-contrast neon"]
LAYOUTS = ["bento-grid", "single-column narrative", "split-hero with timeline", "interactive card deck"]
TYPOGRAPHY = ["Geist & JetBrains Mono", "Inter & Fira Code", "Playfair & Neue Haas", "Clash Display & Satoshi"]
PALETTES = [
    {"bg": "#09090b", "surface": "#18181b", "accent": "#6366f1", "name": "Deep Indigo"},
    {"bg": "#030712", "surface": "#111827", "accent": "#10b981", "name": "Emerald Night"},
    {"bg": "#0f172a", "surface": "#1e293b", "accent": "#38bdf8", "name": "Cyan Deep"},
    {"bg": "#18181b", "surface": "#27272a", "accent": "#f59e0b", "name": "Amber Glow"}
]

TASK_TEMPLATES = [
    {
        "category": "navigation",
        "task_name": "Fix route mismatch in navigation button",
        "symptom": "Navbar button points to invalid route {broken_route} returning 404 instead of active {correct_route}",
        "broken_route": "/contact-us",
        "correct_route": "/contact",
        "target_file": "components/Navbar.tsx",
        "diagnosis": "Route mismatch: Navbar component references non-existent route '{broken_route}' while valid route folder is '{correct_route}'.",
        "fix_diff": "- href='{broken_route}'\n+ href='{correct_route}'",
        "tests": ["level1_static", "level2_build", "level4_browser_click"]
    },
    {
        "category": "accessibility",
        "task_name": "Add missing accessible labels and ARIA landmark to header",
        "symptom": "Accessibility audit reports missing aria-label on navigation landmark and missing alt attributes",
        "broken_route": "/",
        "correct_route": "/",
        "target_file": "components/Navbar.tsx",
        "diagnosis": "WCAG AA violation: <nav> tag lacks descriptive aria-label and icon buttons lack aria-label attributes.",
        "fix_diff": "- <nav className=\"flex items-center\">\n+ <nav aria-label=\"Main Navigation\" className=\"flex items-center\">",
        "tests": ["level1_static", "level7_accessibility"]
    },
    {
        "category": "responsive",
        "task_name": "Fix mobile layout overflow in hero section",
        "symptom": "Mobile viewport (375px) shows horizontal scrollbar and button clipping",
        "broken_route": "/",
        "correct_route": "/",
        "target_file": "components/Hero.tsx",
        "diagnosis": "Fixed width containers or non-wrapping flex row causing horizontal overflow on viewport widths under 640px.",
        "fix_diff": "- <div className=\"flex flex-row gap-4 w-[600px]\">\n+ <div className=\"flex flex-wrap sm:flex-nowrap gap-4 w-full max-w-xl\">",
        "tests": ["level1_static", "level5_responsive"]
    },
    {
        "category": "performance",
        "task_name": "Optimize hero asset loading priority",
        "symptom": "Lighthouse audit flags Largest Contentful Paint (LCP) delay on hero graphic",
        "broken_route": "/",
        "correct_route": "/",
        "target_file": "components/Hero.tsx",
        "diagnosis": "Hero image missing priority attribute causing deferred lazy-loading of above-the-fold visual.",
        "fix_diff": "- <Image src=\"/hero.png\" width={{800}} height={{600}} alt=\"Hero\" />\n+ <Image src=\"/hero.png\" width={{800}} height={{600}} alt=\"Hero\" priority />",
        "tests": ["level1_static", "level2_build", "level6_performance"]
    }
]

def generate_synthetic_dataset(count: int = 50) -> List[Dict[str, Any]]:
    dataset = []
    
    for i in range(count):
        tmpl = random.choice(TASK_TEMPLATES)
        ind = random.choice(INDUSTRIES)
        prof = random.choice(PROFESSIONS)
        style = random.choice(STYLES)
        layout = random.choice(LAYOUTS)
        palette = random.choice(PALETTES)
        typo = random.choice(TYPOGRAPHY)

        task_desc = f"{tmpl['task_name']} for {prof} ({ind}) portfolio in {style} style"
        symptom_text = tmpl["symptom"].format(
            broken_route=tmpl.get("broken_route", "/contact-us"),
            correct_route=tmpl.get("correct_route", "/contact")
        )
        diagnosis_text = tmpl["diagnosis"].format(
            broken_route=tmpl.get("broken_route", "/contact-us"),
            correct_route=tmpl.get("correct_route", "/contact")
        )
        fix_diff = tmpl["fix_diff"].format(
            broken_route=tmpl.get("broken_route", "/contact-us"),
            correct_route=tmpl.get("correct_route", "/contact")
        )

        entry = {
            "trajectory_id": f"traj_synth_{i+1:04d}",
            "domain": "portfolio",
            "task": task_desc,
            "specification": {
                "industry": ind,
                "profession": prof,
                "style": style,
                "layout": layout,
                "color_palette": palette,
                "typography": typo
            },
            "project_context": f"Next.js 14 App Router, Tailwind CSS, TypeScript. Theme: {palette['name']}.",
            "plan": f"1. Main Agent decomposes symptom. 2. Debug Agent analyzes {tmpl['target_file']}. 3. Code Agent applies minimal patch. 4. Test Agent verifies with {', '.join(tmpl['tests'])}.",
            "files_changed": [tmpl["target_file"]],
            "code_changes": [
                {
                    "file": tmpl["target_file"],
                    "action": "minimal_replace",
                    "diff": fix_diff
                }
            ],
            "tests": tmpl["tests"],
            "failures": [
                {
                    "attempt": 1,
                    "error": symptom_text,
                    "diagnosis": diagnosis_text
                }
            ],
            "fixes": [
                {
                    "attempt": 2,
                    "fix_applied": fix_diff,
                    "result": "pass"
                }
            ],
            "final_status": "passed",
            "validation_verified": True,
            "provenance": {
                "generator": "Ornàment Synthetic Engine v1.0",
                "license": "Apache-2.0 / MIT Compatible",
                "timestamp": "2026-09-27T09:30:00Z"
            }
        }
        dataset.append(entry)

    return dataset

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic dataset for Ornàment")
    parser.add_argument("--count", type=int, default=100, help="Number of trajectories to generate")
    parser.add_argument("--output", default="datasets/synthetic_portfolio_v0.2.0.json")
    args = parser.parse_args()

    base = Path(__file__).resolve().parent.parent
    out_file = base / args.output
    out_file.parent.mkdir(parents=True, exist_ok=True)

    print(f"[*] Generating {args.count} synthetic engineering trajectories...")
    data = generate_synthetic_dataset(args.count)

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[OK] Generated {len(data)} trajectories saved to: {out_file}")

if __name__ == "__main__":
    main()
