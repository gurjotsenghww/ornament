"""
Diverse HTML Generator for the Ornàment Training Data System (Sections 5, 18, 19).
Synthesizes high-quality, semantic, accessible HTML+Tailwind components and complete pages across 20 categories.
"""

import random
from typing import List, Dict, Any

# Palette themes for styling variety
THEME_PALETTES = [
    {"name": "dark_indigo", "bg": "bg-[#09090b]", "card": "bg-zinc-900/60 border border-zinc-800", "accent": "text-indigo-400", "btn": "bg-indigo-600 hover:bg-indigo-500 text-white"},
    {"name": "neon_emerald", "bg": "bg-[#06110d]", "card": "bg-emerald-950/20 border border-emerald-900/50", "accent": "text-emerald-400", "btn": "bg-emerald-600 hover:bg-emerald-500 text-black font-bold"},
    {"name": "high_tech_cyan", "bg": "bg-slate-950", "card": "bg-slate-900/70 border border-slate-800", "accent": "text-cyan-400", "btn": "bg-cyan-600 hover:bg-cyan-500 text-white"},
    {"name": "amber_editorial", "bg": "bg-stone-950", "card": "bg-stone-900/60 border border-stone-800", "accent": "text-amber-400", "btn": "bg-amber-600 hover:bg-amber-500 text-white"},
    {"name": "luxury_monochrome", "bg": "bg-black", "card": "bg-zinc-900/80 border border-zinc-800", "accent": "text-zinc-200", "btn": "bg-white hover:bg-zinc-200 text-black font-semibold"},
    {"name": "clean_light", "bg": "bg-slate-50", "card": "bg-white border border-slate-200 shadow-sm", "accent": "text-blue-600", "btn": "bg-blue-600 hover:bg-blue-700 text-white"}
]

# Specialized category builders
def _build_hero(idx: int, pal: Dict[str, str]) -> str:
    headlines = [
        "Architecting Autonomous Agentic Systems at Scale",
        "Deterministic High-Performance Web Engineering",
        "Next-Generation Intelligent Design Systems",
        "Zero-Runtime-Regression Software Architecture",
        "Ultra-Low-Latency Edge Computing Solutions"
    ]
    subheads = [
        "Engineered with surgical minimal diffs, multi-level Playwright verification, and WCAG accessibility compliance.",
        "Delivering resilient local-first applications with automated self-healing compilers and observability.",
        "Empowering distributed developer fleets with verified code synthesis and hardware-aware concurrency."
    ]
    h = headlines[idx % len(headlines)]
    s = subheads[idx % len(subheads)]
    return f"""<header class="w-full border-b border-zinc-800/80 bg-zinc-950/80 backdrop-blur-md sticky top-0 z-50">
  <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
    <a href="/" class="font-extrabold text-white text-lg tracking-tight">Ornàment<span class="{pal['accent']}">.dev</span></a>
    <nav aria-label="Primary" class="hidden md:flex items-center space-x-6 text-sm text-zinc-400">
      <a href="#features" class="hover:text-white transition">Features</a>
      <a href="#pricing" class="hover:text-white transition">Pricing</a>
      <a href="#about" class="hover:text-white transition">About</a>
      <a href="/contact" class="px-4 py-2 rounded-full {pal['btn']} text-xs font-semibold shadow-md">Get Started</a>
    </nav>
  </div>
</header>
<main class="relative overflow-hidden py-24 {pal['bg']} text-white">
  <div class="max-w-5xl mx-auto px-6 text-center space-y-6">
    <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-semibold bg-zinc-900 border border-zinc-800 {pal['accent']}">
      <span class="w-2 h-2 rounded-full bg-current animate-pulse"></span>
      <span>Autonomous Release v{idx % 5 + 1}.0</span>
    </div>
    <h1 class="text-4xl sm:text-6xl font-black tracking-tight leading-tight text-white">{h}</h1>
    <p class="text-lg text-zinc-400 max-w-2xl mx-auto leading-relaxed">{s}</p>
    <div class="flex flex-wrap items-center justify-center gap-4 pt-4">
      <a href="/get-started" class="px-6 py-3 rounded-xl {pal['btn']} text-sm font-bold shadow-lg transition">Deploy Fleet</a>
      <a href="#features" class="px-6 py-3 rounded-xl bg-zinc-900 hover:bg-zinc-800 text-zinc-300 text-sm font-semibold border border-zinc-800 transition">Explore Architecture</a>
    </div>
  </div>
</main>"""

def _build_cards(idx: int, pal: Dict[str, str]) -> str:
    return f"""<section class="py-16 {pal['bg']} text-zinc-100">
  <div class="max-w-7xl mx-auto px-6">
    <div class="text-center max-w-2xl mx-auto mb-12">
      <h2 class="text-xs uppercase font-mono tracking-widest {pal['accent']} mb-2">Engineered Modules</h2>
      <h3 class="text-3xl font-extrabold text-white">Core Architectural Building Blocks</h3>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <article class="p-6 rounded-2xl {pal['card']} hover:border-zinc-700 transition flex flex-col justify-between">
        <div>
          <div class="w-10 h-10 rounded-xl bg-zinc-800 flex items-center justify-center {pal['accent']} font-bold mb-4">01</div>
          <h4 class="text-xl font-bold text-white mb-2">Minimal Change Engine</h4>
          <p class="text-sm text-zinc-400 leading-relaxed">Isolates root cause anomalies and applies surgical 1-file diffs while strictly preserving working production logic.</p>
        </div>
        <div class="mt-6 pt-4 border-t border-zinc-800/80 flex items-center justify-between text-xs text-zinc-500">
          <span>Module v1.{idx}</span>
          <span class="{pal['accent']}">Verified [OK]</span>
        </div>
      </article>
      <article class="p-6 rounded-2xl {pal['card']} hover:border-zinc-700 transition flex flex-col justify-between">
        <div>
          <div class="w-10 h-10 rounded-xl bg-zinc-800 flex items-center justify-center {pal['accent']} font-bold mb-4">02</div>
          <h4 class="text-xl font-bold text-white mb-2">Multi-Level Playwright Tests</h4>
          <p class="text-sm text-zinc-400 leading-relaxed">Levels 1 through 7 static compilation, build validation, browser DOM verification, and full WCAG accessibility audits.</p>
        </div>
        <div class="mt-6 pt-4 border-t border-zinc-800/80 flex items-center justify-between text-xs text-zinc-500">
          <span>Suite 7-Tier</span>
          <span class="{pal['accent']}">100% Pass</span>
        </div>
      </article>
      <article class="p-6 rounded-2xl {pal['card']} hover:border-zinc-700 transition flex flex-col justify-between">
        <div>
          <div class="w-10 h-10 rounded-xl bg-zinc-800 flex items-center justify-center {pal['accent']} font-bold mb-4">03</div>
          <h4 class="text-xl font-bold text-white mb-2">Hardware-Gated Concurrency</h4>
          <p class="text-sm text-zinc-400 leading-relaxed">Monitors GPU VRAM and system memory in real time to throttle subagent concurrency and prevent thrashing.</p>
        </div>
        <div class="mt-6 pt-4 border-t border-zinc-800/80 flex items-center justify-between text-xs text-zinc-500">
          <span>VRAM Guard</span>
          <span class="{pal['accent']}">Safe 6GB</span>
        </div>
      </article>
    </div>
  </div>
</section>"""

def _build_pricing(idx: int, pal: Dict[str, str]) -> str:
    return f"""<section id="pricing" class="py-20 {pal['bg']} text-zinc-100 border-t border-zinc-800/80">
  <div class="max-w-7xl mx-auto px-6">
    <div class="text-center max-w-2xl mx-auto mb-16">
      <h2 class="text-xs uppercase font-mono tracking-widest {pal['accent']} mb-2">Tiered Deployment</h2>
      <h3 class="text-3xl font-extrabold text-white">Transparent Autonomous Computing</h3>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div class="p-8 rounded-2xl {pal['card']} flex flex-col justify-between">
        <div>
          <h4 class="text-lg font-bold text-white">Local Developer</h4>
          <div class="text-3xl font-black text-white mt-4">$0 <span class="text-sm font-normal text-zinc-400">/ forever</span></div>
          <p class="text-xs text-zinc-400 mt-2">Single workstation deployment on local GPU with GGUF 4-bit inference.</p>
          <ul class="mt-6 space-y-3 text-xs text-zinc-300">
            <li class="flex items-center space-x-2"><span>[OK]</span><span>Zero-cloud local execution</span></li>
            <li class="flex items-center space-x-2"><span>[OK]</span><span>Git Checkpoint rollbacks</span></li>
            <li class="flex items-center space-x-2"><span>[OK]</span><span>Playwright DOM test suite</span></li>
          </ul>
        </div>
        <button class="mt-8 w-full py-2.5 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-white font-semibold text-xs border border-zinc-700">Deploy Local</button>
      </div>
      <div class="p-8 rounded-2xl {pal['card']} relative border-2 border-indigo-500/50 shadow-2xl flex flex-col justify-between">
        <div class="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full bg-indigo-600 text-white text-[10px] font-bold uppercase tracking-wider">Recommended</div>
        <div>
          <h4 class="text-lg font-bold text-white">Autonomous Fleet</h4>
          <div class="text-3xl font-black text-white mt-4">$49 <span class="text-sm font-normal text-zinc-400">/ month</span></div>
          <p class="text-xs text-zinc-400 mt-2">Full agentic hierarchy with Debug, Code, and Test agent delegation.</p>
          <ul class="mt-6 space-y-3 text-xs text-zinc-300">
            <li class="flex items-center space-x-2"><span class="{pal['accent']}">[OK]</span><span>Unlimited autonomous repair loops</span></li>
            <li class="flex items-center space-x-2"><span class="{pal['accent']}">[OK]</span><span>Automated LoRA fine-tuning adapters</span></li>
            <li class="flex items-center space-x-2"><span class="{pal['accent']}">[OK]</span><span>Realtime telemetry observability</span></li>
          </ul>
        </div>
        <button class="mt-8 w-full py-2.5 rounded-xl {pal['btn']} text-xs font-bold shadow-lg">Start Free Trial</button>
      </div>
      <div class="p-8 rounded-2xl {pal['card']} flex flex-col justify-between">
        <div>
          <h4 class="text-lg font-bold text-white">Enterprise Edge</h4>
          <div class="text-3xl font-black text-white mt-4">$299 <span class="text-sm font-normal text-zinc-400">/ month</span></div>
          <p class="text-xs text-zinc-400 mt-2">Dedicated cluster nodes with enterprise SLA and custom model adapters.</p>
          <ul class="mt-6 space-y-3 text-xs text-zinc-300">
            <li class="flex items-center space-x-2"><span>[OK]</span><span>Air-gapped on-premise installation</span></li>
            <li class="flex items-center space-x-2"><span>[OK]</span><span>Dedicated GPU training pipeline</span></li>
            <li class="flex items-center space-x-2"><span>[OK]</span><span>Continuous Playwright CI integration</span></li>
          </ul>
        </div>
        <button class="mt-8 w-full py-2.5 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-white font-semibold text-xs border border-zinc-700">Contact Sales</button>
      </div>
    </div>
  </div>
</section>"""

def _build_form(idx: int, pal: Dict[str, str]) -> str:
    return f"""<section id="contact" class="py-16 {pal['bg']} text-zinc-100">
  <div class="max-w-xl mx-auto px-6">
    <div class="text-center mb-8">
      <h2 class="text-xs uppercase font-mono tracking-widest {pal['accent']} mb-2">Initiate Dispatch</h2>
      <h3 class="text-3xl font-extrabold text-white">Connect with Autonomous Engineering</h3>
    </div>
    <form class="space-y-4 {pal['card']} p-8 rounded-2xl shadow-xl">
      <div>
        <label for="name-{idx}" class="block text-xs font-semibold text-zinc-400 mb-1">Your Name</label>
        <input id="name-{idx}" name="name" type="text" placeholder="Alex Vance" required class="w-full p-2.5 rounded-lg bg-zinc-800 border border-zinc-700 text-white text-xs focus:outline-none focus:border-indigo-500" />
      </div>
      <div>
        <label for="email-{idx}" class="block text-xs font-semibold text-zinc-400 mb-1">Work Email</label>
        <input id="email-{idx}" name="email" type="email" placeholder="alex@ornament.ai" required class="w-full p-2.5 rounded-lg bg-zinc-800 border border-zinc-700 text-white text-xs focus:outline-none focus:border-indigo-500" />
      </div>
      <div>
        <label for="message-{idx}" class="block text-xs font-semibold text-zinc-400 mb-1">Engineering Specifications</label>
        <textarea id="message-{idx}" name="message" rows="4" placeholder="Describe requirements, target framework, and test assertions..." required class="w-full p-2.5 rounded-lg bg-zinc-800 border border-zinc-700 text-white text-xs focus:outline-none focus:border-indigo-500"></textarea>
      </div>
      <button type="submit" class="w-full py-3 rounded-xl {pal['btn']} text-xs font-bold shadow-md transition">Dispatch Autonomous Agents</button>
    </form>
  </div>
</section>"""

def _build_portfolio(idx: int, domain: str, style: str, pal: Dict[str, str]) -> str:
    names = ["Kaelen Thorne", "Dr. Samantha Reed", "Elena Rostova", "Marcus Chen", "Aria Sterling"]
    titles = {
        "developer": "Lead Autonomous Systems Architect",
        "designer": "Principal Digital Product & UX Designer",
        "founder": "Founder & Technical Operator",
        "photographer": "Architectural & Cinematic Photographer",
        "creative": "Creative Technologist & Interactive Director",
        "product_manager": "Principal AI Platform Product Manager",
        "three_d": "3D Generative Realtime Graphics Artist",
        "agency": "High-Performance Autonomous Studio"
    }
    name = names[idx % len(names)]
    title = titles.get(domain, "Senior Web Engineer")

    return f"""<header class="w-full border-b border-zinc-800 bg-zinc-950/80 backdrop-blur-md sticky top-0 z-50">
  <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
    <a href="/" class="font-extrabold text-white text-lg tracking-tight">{name}<span class="{pal['accent']}">.</span></a>
    <nav aria-label="Main Navigation" class="flex items-center space-x-6 text-sm">
      <a href="#work" class="text-zinc-400 hover:text-white transition">Work</a>
      <a href="#about" class="text-zinc-400 hover:text-white transition">About</a>
      <a id="nav-contact-button" href="/contact" class="px-4 py-2 rounded-full {pal['btn']} text-xs font-semibold">Contact</a>
    </nav>
  </div>
</header>
<main class="max-w-6xl mx-auto px-6 py-20 {pal['bg']} text-zinc-100 space-y-16">
  <section class="space-y-6 max-w-3xl">
    <div class="inline-flex items-center space-x-2 text-xs font-mono {pal['accent']} bg-zinc-900 px-3 py-1 rounded-full border border-zinc-800">
      <span class="w-2 h-2 rounded-full bg-current"></span>
      <span>{style.title()} Portfolio • {domain.replace('_', ' ').title()}</span>
    </div>
    <h1 class="text-4xl sm:text-6xl font-black text-white tracking-tight leading-tight">
      {name} — {title}.
    </h1>
    <p class="text-lg text-zinc-400 leading-relaxed">
      Specializing in resilient distributed architectures, minimal change self-healing systems, and responsive modern web engineering.
    </p>
    <div class="pt-2">
      <a href="#work" class="px-6 py-3 rounded-xl {pal['btn']} text-xs font-bold shadow-lg">View Selected Projects</a>
    </div>
  </section>
  <section id="work" class="space-y-8">
    <h2 class="text-2xl font-bold text-white border-b border-zinc-800 pb-3">Selected Projects</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <article class="p-6 rounded-2xl {pal['card']} hover:border-zinc-700 transition">
        <span class="text-xs font-mono {pal['accent']}">01 / AUTONOMOUS WEB</span>
        <h3 class="text-xl font-bold text-white mt-1 mb-2">Ornàment Agent Engine</h3>
        <p class="text-xs text-zinc-400 leading-relaxed">Full lifecycle AI website engineer adhering strictly to minimal change policy and Playwright test validation.</p>
      </article>
      <article class="p-6 rounded-2xl {pal['card']} hover:border-zinc-700 transition">
        <span class="text-xs font-mono {pal['accent']}">02 / EDGE INFERENCE</span>
        <h3 class="text-xl font-bold text-white mt-1 mb-2">Quantized Coder Cluster</h3>
        <p class="text-xs text-zinc-400 leading-relaxed">Local-first 4-bit GGUF model execution pipeline operating within 6GB VRAM hardware bounds.</p>
      </article>
    </div>
  </section>
</main>
<footer class="border-t border-zinc-800/80 py-8 bg-zinc-950 text-center text-xs text-zinc-500">
  <p>&copy; 2026 {name}. All rights reserved.</p>
</footer>"""

def generate_html(count: int, categories: List[str] = None) -> List[Dict[str, Any]]:
    """
    Generates 'count' high-quality, production-grade HTML examples across categories.
    """
    if not categories:
        categories = ["heroes", "cards", "pricing", "forms", "portfolios", "complete_pages"]

    domains = ["developer", "designer", "founder", "photographer", "creative", "product_manager", "three_d", "agency"]
    styles = ["minimal", "modern", "premium", "luxury", "dark", "light", "futuristic", "editorial", "brutalist", "creative"]

    results = []
    for i in range(count):
        cat = categories[i % len(categories)]
        pal = THEME_PALETTES[i % len(THEME_PALETTES)]
        dom = domains[i % len(domains)]
        sty = styles[i % len(styles)]

        if cat in ["heroes", "headers"]:
            code = _build_hero(i, pal)
            desc = f"Accessible modern hero section with navigation and {pal['name']} theme"
        elif cat in ["cards", "sections"]:
            code = _build_cards(i, pal)
            desc = f"Responsive 3-column feature card grid with {pal['name']} theme"
        elif cat in ["pricing", "tables"]:
            code = _build_pricing(i, pal)
            desc = f"Tiered pricing matrix with recommended badges and {pal['name']} theme"
        elif cat in ["forms", "contact"]:
            code = _build_form(i, pal)
            desc = f"Accessible contact request form with validation styling"
        elif cat in ["portfolios", "complete_pages"]:
            code = _build_portfolio(i, dom, sty, pal)
            desc = f"Complete {sty} portfolio for {dom} with selected works and navigation"
        else:
            code = _build_hero(i, pal)
            desc = f"Semantic HTML component for {cat}"

        results.append({
            "instruction": f"Build a production-quality, accessible {cat} component in {pal['name']} style.",
            "context": {
                "framework": "HTML5 / Tailwind CSS",
                "requirements": ["semantic-html", "responsive", "accessible", pal['name']]
            },
            "output": code,
            "metadata": {
                "category": cat,
                "domain": dom,
                "style": sty,
                "palette": pal["name"],
                "difficulty": "medium" if cat in ["heroes", "cards"] else "advanced",
                "description": desc,
                "source_type": "generated",
                "license": "MIT"
            }
        })

    return results
