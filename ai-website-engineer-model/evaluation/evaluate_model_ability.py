#!/usr/bin/env python3
"""
Ornàment Baseline Model Ability Benchmark.
Evaluates Qwen2.5-Coder-3B across 5 core dimensions:
1. Website Design Theory & Systems (Color, Typography, Spatial Grids, WCAG)
2. Modern Frontend Code Craft (Semantic HTML5, Bento Grids, Glassmorphism, Tailwind)
3. Bug Diagnosis & Minimal Change Policy (Surgical Repair, Exact Replacement)
4. Design Aesthetics & Taste (Transforming generic components to luxury standard)
5. Modern CSS Architecture (clamp(), Container Queries, Custom Properties)

Outputs a comprehensive evaluation JSON and markdown diagnostic report.
"""
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List

def run_evaluation() -> Dict[str, Any]:
    base_dir = Path(__file__).resolve().parent.parent.parent
    weights_path = base_dir / "ai-website-engineer-model" / "weights" / "qwen2.5-coder-3b-instruct-q4_k_m.gguf"
    
    if not weights_path.exists():
        raise FileNotFoundError(f"Model weights not found at: {weights_path}")

    from llama_cpp import Llama
    print(f"[*] Loading model from {weights_path}...")
    start_load = time.time()
    llm = Llama(
        model_path=str(weights_path),
        n_ctx=3072,
        n_threads=4,
        verbose=False
    )
    print(f"[OK] Model loaded in {round(time.time() - start_load, 2)}s\n")

    test_cases = [
        {
            "id": "design_theory",
            "title": "Design Theory & Systems",
            "prompt": (
                "You are an expert website design theorist. "
                "Explain how you apply the 60-30-10 color rule and modular typographic scaling (Major Third vs Perfect Fourth) "
                "in designing an ultra-modern dark luxury portfolio website. What specific contrast ratios and spacing scales do you enforce?"
            ),
            "expected_keywords": ["60", "30", "10", "ratio", "contrast", "wcag", "4.5", "spacing", "scale", "grid"],
            "rubric": {
                "color_rule": "Explains 60% dominant background, 30% structural/cards, 10% accent/CTA",
                "typographic_scale": "Explains modular scale multiplier (e.g. 1.25 for Major Third or 1.333 for Perfect Fourth)",
                "contrast_ratios": "Specifies WCAG AA minimum 4.5:1 for normal text and 3:1 for large/UI components",
                "spatial_system": "Specifies 4px or 8px grid system with consistent spacing tokens"
            }
        },
        {
            "id": "code_craft",
            "title": "Modern Frontend Code Craft",
            "prompt": (
                "Write a semantic HTML5 and Tailwind CSS Bento-grid feature section for a SaaS product. "
                "It must include 3 cards of asymmetrical spans, modern dark glassmorphism effects (backdrop-filter, subtle borders), "
                "and accessible ARIA attributes. Provide production-ready code."
            ),
            "expected_keywords": ["<section", "grid", "col-span", "backdrop-blur", "border", "rounded", "aria-"],
            "rubric": {
                "semantic_html": "Uses <section>, <header>/<h2>, <article> or semantic cards",
                "bento_grid": "Uses CSS Grid with asymmetrical col-span/row-span",
                "glassmorphism": "Uses backdrop-blur, subtle transparent border, semi-transparent dark bg",
                "accessibility": "Includes aria-labelledby or aria-describedby or semantic headings"
            }
        },
        {
            "id": "minimal_change_diagnosis",
            "title": "Bug Diagnosis & Minimal Change Policy",
            "prompt": (
                "You are an autonomous website engineer in the Ornàment system. "
                "You MUST adhere strictly to the Minimal Change Policy: Never rewrite working code, provide ONLY the minimal fix lines.\n\n"
                "Given this broken code:\n"
                "```html\n"
                "<nav class=\"flex items-center justify-between p-4 bg-zinc-900\">\n"
                "  <a href=\"/\" class=\"font-bold text-white\">Brand</a>\n"
                "  <div class=\"space-x-4\">\n"
                "    <a href=\"/about\" class=\"text-zinc-400\">About</a>\n"
                "    <a href=\"/pricing\" class=\"text-zinc-400\">Pricing</a>\n"
                "    <a href=\"/contact-us\" class=\"text-zinc-400\">Contact</a>\n"
                "  </div>\n"
                "</nav>\n"
                "```\n"
                "Problem: The router only serves '/contact', but the link points to '/contact-us', triggering a 404 error.\n"
                "Requirement:\n"
                "1. State the root cause in 1 concise sentence.\n"
                "2. Provide ONLY the exact line replacement (do NOT output the entire file)."
            ),
            "expected_keywords": ["contact", "minimal", "replace", "href"],
            "rubric": {
                "root_cause": "Accurately identifies the route mismatch between /contact-us and /contact",
                "minimal_patch": "Only replaces the single broken line without rewriting the entire navbar",
                "clarity": "Concise and strictly follows instructions"
            }
        },
        {
            "id": "aesthetic_taste",
            "title": "Design Taste & Component Elevation",
            "prompt": (
                "Critique this generic button:\n"
                "`<button style=\"background: blue; color: white; padding: 10px 20px; border-radius: 5px;\">Click Here</button>`\n"
                "How would you transform it into an award-winning, ultra-premium button for a high-end AI product? "
                "Provide the critique and the refined Tailwind CSS code with micro-interactions, gradients, and depth."
            ),
            "expected_keywords": ["hover", "transition", "focus", "gradient", "shadow", "ring", "state"],
            "rubric": {
                "critique_quality": "Identifies lack of hover/focus states, harsh saturated blue, inline styles, lack of depth",
                "aesthetic_elevation": "Adds subtle gradient, border glow or layered shadow, active press feedback, focus ring",
                "typography_craft": "Improves font weight, letter spacing (tracking), or text styling"
            }
        },
        {
            "id": "modern_css_features",
            "title": "Modern CSS Architecture",
            "prompt": (
                "Demonstrate three modern CSS capabilities:\n"
                "1. Fluid typography using clamp()\n"
                "2. A CSS custom property token system for dark/light mode\n"
                "3. A CSS container query (@container) example\n"
                "Briefly explain why container queries are superior to media queries for modular UI components."
            ),
            "expected_keywords": ["clamp", "container", "@container", "--", ":root", "modular"],
            "rubric": {
                "clamp_syntax": "Correctly formats clamp(min, preferred, max)",
                "custom_properties": "Defines CSS variables on :root and dark selector/media",
                "container_queries": "Uses container-type and @container query",
                "architectural_reasoning": "Explains component modularity based on parent container width rather than viewport"
            }
        }
    ]

    system_prompt = (
        "You are Qwen2.5-Coder-3B, the autonomous AI website engineer in the Ornàment system. "
        "You possess deep knowledge of website design theory, Swiss design, visual hierarchy, "
        "semantic HTML5, modern CSS, Tailwind, and surgical bug repair under Ornàment's Minimal Change Policy. "
        "Provide thorough, high-craft, professional answers."
    )

    results = []
    total_score = 0.0

    print("=================================================================")
    print("      ORNÀMENT BASELINE MODEL EVALUATION BATTERY (Qwen2.5-Coder-3B)")
    print("=================================================================\n")

    for i, tc in enumerate(test_cases, 1):
        print(f"[{i}/5] Running Test: {tc['title']} ({tc['id']})...")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": tc["prompt"]}
        ]

        t0 = time.time()
        response = llm.create_chat_completion(
            messages=messages,
            max_tokens=650,
            temperature=0.4
        )
        duration = time.time() - t0
        content = response["choices"][0]["message"]["content"]

        # Automatic keyword & criteria grading
        matched_kw = [kw for kw in tc["expected_keywords"] if kw.lower() in content.lower()]
        kw_coverage = len(matched_kw) / len(tc["expected_keywords"])
        
        # Scoring logic
        raw_score = min(100.0, round(kw_coverage * 100.0, 1))
        # Extra heuristic bonuses based on length and structure
        if len(content.split()) > 60:
            raw_score = min(100.0, raw_score + 10.0)
        if "```" in content:
            raw_score = min(100.0, raw_score + 5.0)

        total_score += raw_score

        test_result = {
            "test_id": tc["id"],
            "title": tc["title"],
            "prompt": tc["prompt"],
            "response": content,
            "duration_seconds": round(duration, 2),
            "matched_keywords": matched_kw,
            "keyword_coverage": round(kw_coverage, 2),
            "score": round(raw_score, 1),
            "rubric": tc["rubric"]
        }
        results.append(test_result)
        print(f"    Done in {round(duration, 2)}s | Score: {raw_score}/100 | Keywords matched: {len(matched_kw)}/{len(tc['expected_keywords'])}\n")

    overall_average = round(total_score / len(test_cases), 1)

    summary = {
        "model_name": "Qwen2.5-Coder-3B-Instruct",
        "format": "GGUF Q4_K_M",
        "evaluation_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "overall_score": overall_average,
        "results": results
    }

    output_json = base_dir / "ai-website-engineer-model" / "evaluation" / "baseline_ability_report.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"=================================================================")
    print(f"OVERALL BASELINE BENCHMARK SCORE: {overall_average} / 100")
    print(f"Full report saved to: {output_json}")
    print(f"=================================================================")

    return summary

if __name__ == "__main__":
    run_evaluation()
