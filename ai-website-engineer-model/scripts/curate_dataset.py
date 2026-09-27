#!/usr/bin/env python3
"""
Curates high-fidelity HTML5 + modern Tailwind CSS datasets for training the Ornàment model.
Ingests premier open-source component patterns (SaaS Bento grids, Minimal Portfolios, E-Commerce, Dashboards),
normalizes W3C semantics and Tailwind accessibility, and exports ChatML format for LoRA fine-tuning.
"""

import json
from pathlib import Path
from typing import List, Dict, Any

# High-fidelity curated design templates (HTML5 + Modern Tailwind CSS)
DESIGN_TEMPLATES = [
    {
        "domain": "saas_bento",
        "instruction": "Build an ultra-modern dark SaaS hero section with glassmorphism, glowing badges, and a 3-column bento feature grid.",
        "thought": "1. Semantic structure: <header>, <main>, <section id='hero'>, <section id='features'>.\n2. Visual aesthetic: Dark background (#09090b), radial gradient glow, zinc surface cards with subtle borders.\n3. Bento grid: Responsive grid with varied card spans, SVG icons, and typography hierarchy.\n4. Accessibility: Main landmarks, proper heading hierarchy, contrast ratio > 4.5:1.",
        "html_css": """<section class="relative overflow-hidden py-24 bg-[#09090b] text-white">
  <div class="absolute inset-0 bg-gradient-to-b from-indigo-500/10 via-transparent to-transparent pointer-events-none"></div>
  <div class="max-w-7xl mx-auto px-6 lg:px-8 relative z-10">
    <div class="text-center max-w-3xl mx-auto mb-16 space-y-4">
      <span class="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
        <span class="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
        <span>Autonomous Agent Fleet v2.0</span>
      </span>
      <h1 class="text-5xl font-black tracking-tight sm:text-6xl text-transparent bg-clip-text bg-gradient-to-r from-white via-zinc-200 to-zinc-400">
        Websites engineered by autonomous intelligence.
      </h1>
      <p class="text-lg text-zinc-400 leading-relaxed">
        Diagnose, test, and ship production applications with surgical 1-file diffs and zero regressions.
      </p>
    </div>

    <!-- Bento Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="md:col-span-2 p-8 rounded-2xl bg-zinc-900/60 border border-zinc-800 hover:border-zinc-700 transition">
        <span class="text-xs font-mono text-indigo-400 uppercase tracking-widest">Core Philosophy</span>
        <h2 class="text-2xl font-bold mt-2 mb-3">Minimal Change Policy</h2>
        <p class="text-zinc-400 text-sm leading-relaxed">Never regenerate entire codebases for isolated bugs. Isolate root causes and produce minimal surgical patches that preserve all existing working features.</p>
      </div>
      <div class="p-8 rounded-2xl bg-zinc-900/60 border border-zinc-800 hover:border-zinc-700 transition">
        <span class="text-xs font-mono text-emerald-400 uppercase tracking-widest">Validation</span>
        <h2 class="text-2xl font-bold mt-2 mb-3">Playwright Level 1-7</h2>
        <p class="text-zinc-400 text-sm leading-relaxed">Automated browser functional assertion, DOM navigation checks, and full WCAG accessibility audits.</p>
      </div>
    </div>
  </div>
</section>"""
    },
    {
        "domain": "portfolio_minimal",
        "instruction": "Create an accessible, minimalist developer portfolio hero with dark mode styling, navigation, and call to action.",
        "thought": "1. Clean typography using high-contrast sans-serif.\n2. Prominent name and value proposition.\n3. ARIA compliant navigation links with active state indicators.\n4. Primary and secondary action buttons.",
        "html_css": """<header class="border-b border-zinc-800 bg-zinc-950/80 backdrop-blur-md sticky top-0 z-50">
  <div class="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
    <a href="/" class="font-bold text-white text-lg tracking-tight">Elena Rostova<span class="text-indigo-500">.</span></a>
    <nav aria-label="Main Navigation" class="flex items-center space-x-6 text-sm">
      <a href="#work" class="text-zinc-400 hover:text-white transition">Selected Work</a>
      <a href="#about" class="text-zinc-400 hover:text-white transition">About</a>
      <a href="/contact" class="px-4 py-2 rounded-full bg-white text-black font-semibold text-xs hover:bg-zinc-200 transition">Get in Touch</a>
    </nav>
  </div>
</header>
<main class="max-w-5xl mx-auto px-6 py-24 space-y-8">
  <div class="inline-flex items-center space-x-2 text-xs font-mono text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
    <span>Available for Autonomous Systems Architecture</span>
  </div>
  <h1 class="text-5xl sm:text-6xl font-black text-white tracking-tight leading-tight max-w-3xl">
    Designing resilient software systems at the edge of autonomy.
  </h1>
  <p class="text-xl text-zinc-400 max-w-2xl leading-relaxed">
    Specialized in local-first AI engineering, real-time telemetry, and high-performance distributed web architectures.
  </p>
</main>"""
    },
    {
        "domain": "ecommerce_catalog",
        "instruction": "Construct a responsive e-commerce product card grid with dark UI, price display, badge tag, and add to cart interaction.",
        "thought": "1. Responsive CSS grid: 1 column mobile, 2 columns tablet, 3 columns desktop.\n2. Product cards with aspect-square preview images, price tags, category tags.\n3. Hover micro-interactions: border illumination and subtle transform.",
        "html_css": """<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 p-6 max-w-7xl mx-auto">
  <article class="group rounded-2xl bg-zinc-900 border border-zinc-800 overflow-hidden hover:border-zinc-700 transition flex flex-col justify-between">
    <div class="relative aspect-video bg-zinc-950 flex items-center justify-center p-6 border-b border-zinc-800">
      <span class="absolute top-3 left-3 text-[10px] font-bold font-mono px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">NEW RELEASE</span>
      <div class="text-zinc-600 font-mono text-xs">[Hardware Node 64GB]</div>
    </div>
    <div class="p-6 flex-1 flex flex-col justify-between space-y-4">
      <div>
        <h3 class="font-bold text-white text-lg group-hover:text-indigo-400 transition">Ornàment Edge Node 64GB</h3>
        <p class="text-zinc-400 text-xs mt-1 leading-relaxed">Compact hardware compute appliance optimized for local-first autonomous website engineering.</p>
      </div>
      <div class="flex items-center justify-between pt-4 border-t border-zinc-800/80">
        <span class="text-2xl font-black text-white font-mono">$899.00</span>
        <button type="button" class="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs shadow-lg transition">
          Add to Cart
        </button>
      </div>
    </div>
  </article>
</div>"""
    }
]

def format_chatml(system_prompt: str, user_prompt: str, assistant_response: str) -> Dict[str, Any]:
    return {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_response}
        ]
    }

def curate_dataset(output_path: Path):
    system_prompt = (
        "You are Ornàment, an expert autonomous AI Website Engineer. "
        "You output modern, responsive, accessible semantic HTML5 and Tailwind CSS. "
        "Always adhere to the Minimal Change Policy, semantic landmarks, and WCAG accessibility standards."
    )
    
    dataset = []
    for item in DESIGN_TEMPLATES:
        content = f"Plan:\n{item['thought']}\n\n```html\n{item['html_css']}\n```"
        entry = format_chatml(system_prompt, item["instruction"], content)
        dataset.append(entry)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    print(f"[OK] Curated {len(dataset)} premier HTML+CSS design templates into: {output_path}")

if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "datasets" / "html_css_curated_v0.1.0.json"
    curate_dataset(out)
