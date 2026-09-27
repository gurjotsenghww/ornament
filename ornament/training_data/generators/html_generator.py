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

def _build_dashboard(idx: int, pal: Dict[str, str]) -> str:
    return f"""<main class="min-h-screen {pal['bg']} text-zinc-100 p-6 md:p-10 space-y-8">
  <header class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-zinc-800">
    <div>
      <h1 class="text-2xl font-black text-white tracking-tight">Autonomous Cluster Telemetry</h1>
      <p class="text-xs text-zinc-400 mt-1">Real-time hardware saturation and agent dispatch queue.</p>
    </div>
    <div class="flex items-center space-x-3">
      <span class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-950/40 text-emerald-400 border border-emerald-800/60">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span>VRAM Safe: 3.85 GB / 6.0 GB</span>
      </span>
      <button class="px-4 py-2 rounded-xl {pal['btn']} text-xs font-bold shadow-md">Deploy Adapter</button>
    </div>
  </header>
  <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
    <div class="p-6 rounded-2xl {pal['card']}">
      <span class="text-xs font-mono text-zinc-400">Total Validated Samples</span>
      <div class="text-3xl font-black text-white mt-2">15,420</div>
      <div class="mt-4 flex items-center text-xs {pal['accent']}"><span>+18.4%</span><span class="text-zinc-500 ml-1.5">vs previous iteration</span></div>
    </div>
    <div class="p-6 rounded-2xl {pal['card']}">
      <span class="text-xs font-mono text-zinc-400">Self-Healing Pass Rate</span>
      <div class="text-3xl font-black text-emerald-400 mt-2">100%</div>
      <div class="mt-4 text-xs text-zinc-500">21 of 21 test suites passing</div>
    </div>
    <div class="p-6 rounded-2xl {pal['card']}">
      <span class="text-xs font-mono text-zinc-400">Inference Latency</span>
      <div class="text-3xl font-black text-white mt-2">48 ms</div>
      <div class="mt-4 text-xs text-zinc-500">Local RTX 3050 Tensor Cores</div>
    </div>
    <div class="p-6 rounded-2xl {pal['card']}">
      <span class="text-xs font-mono text-zinc-400">Deduplication Ratio</span>
      <div class="text-3xl font-black text-cyan-400 mt-2">3.2x</div>
      <div class="mt-4 text-xs text-zinc-500">179 duplicates skipped</div>
    </div>
  </div>
</main>"""

def _build_ecommerce(idx: int, pal: Dict[str, str]) -> str:
    return f"""<section class="py-16 {pal['bg']} text-zinc-100">
  <div class="max-w-7xl mx-auto px-6 space-y-10">
    <div class="flex items-end justify-between border-b border-zinc-800 pb-4">
      <div>
        <span class="text-xs font-mono {pal['accent']} uppercase tracking-widest">Hardware Catalog</span>
        <h2 class="text-3xl font-extrabold text-white mt-1">Autonomous Edge Compute Modules</h2>
      </div>
      <a href="/catalog" class="text-xs font-semibold text-zinc-400 hover:text-white transition">View All Products &rarr;</a>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      <article class="p-5 rounded-2xl {pal['card']} flex flex-col justify-between group">
        <div>
          <div class="w-full h-44 rounded-xl bg-zinc-800/80 mb-4 flex items-center justify-center text-zinc-600 font-mono text-xs">
            [High-Density Edge Node v{idx + 1}]
          </div>
          <div class="flex items-center justify-between text-xs text-zinc-400 mb-1">
            <span class="{pal['accent']}">Verified Hardware</span>
            <span>4C / 8T • 6GB VRAM</span>
          </div>
          <h3 class="text-lg font-bold text-white group-hover:text-indigo-400 transition">Ornàment Edge Node Pro</h3>
          <p class="text-xs text-zinc-400 mt-2 leading-relaxed">Dedicated local neural inference workstation engineered for deterministic Playwright browser testing.</p>
        </div>
        <div class="mt-6 pt-4 border-t border-zinc-800/80 flex items-center justify-between">
          <div class="text-xl font-black text-white">$1,299</div>
          <button class="px-4 py-2 rounded-xl {pal['btn']} text-xs font-bold shadow-md">Add to Cart</button>
        </div>
      </article>
      <article class="p-5 rounded-2xl {pal['card']} flex flex-col justify-between group">
        <div>
          <div class="w-full h-44 rounded-xl bg-zinc-800/80 mb-4 flex items-center justify-center text-zinc-600 font-mono text-xs">
            [Thermal Accelerator Module]
          </div>
          <div class="flex items-center justify-between text-xs text-zinc-400 mb-1">
            <span class="{pal['accent']}">Thermal Guard</span>
            <span>Zero-Throttle Cryo</span>
          </div>
          <h3 class="text-lg font-bold text-white group-hover:text-indigo-400 transition">CryoShield GPU Coolant Plate</h3>
          <p class="text-xs text-zinc-400 mt-2 leading-relaxed">Precision vapor chamber cooling block maintaining continuous 65°C under sustained LoRA fine-tuning.</p>
        </div>
        <div class="mt-6 pt-4 border-t border-zinc-800/80 flex items-center justify-between">
          <div class="text-xl font-black text-white">$149</div>
          <button class="px-4 py-2 rounded-xl {pal['btn']} text-xs font-bold shadow-md">Add to Cart</button>
        </div>
      </article>
    </div>
  </div>
</section>"""

def _build_footer(idx: int, pal: Dict[str, str]) -> str:
    return f"""<footer class="border-t border-zinc-800/80 bg-zinc-950 text-zinc-400 py-16">
  <div class="max-w-7xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8">
    <div class="space-y-3 col-span-2 md:col-span-1">
      <span class="text-lg font-extrabold text-white">Ornàment<span class="{pal['accent']}">.dev</span></span>
      <p class="text-xs text-zinc-500 leading-relaxed">Autonomous AI Website Engineer with deterministic verification, hardware-bound concurrency, and minimal change policy.</p>
    </div>
    <div>
      <h3 class="text-xs font-bold text-white uppercase tracking-wider mb-3">Architecture</h3>
      <ul class="space-y-2 text-xs">
        <li><a href="/specs" class="hover:text-white transition">Agent Hierarchy</a></li>
        <li><a href="/testing" class="hover:text-white transition">7-Level Test Suite</a></li>
        <li><a href="/sandbox" class="hover:text-white transition">Safe Sandbox Files</a></li>
      </ul>
    </div>
    <div>
      <h3 class="text-xs font-bold text-white uppercase tracking-wider mb-3">Model Engine</h3>
      <ul class="space-y-2 text-xs">
        <li><a href="/models" class="hover:text-white transition">Qwen2.5-Coder 3B</a></li>
        <li><a href="/lora" class="hover:text-white transition">4-bit QLoRA Pipeline</a></li>
        <li><a href="/training-data" class="hover:text-white transition">Instruction Datasets</a></li>
      </ul>
    </div>
    <div>
      <h3 class="text-xs font-bold text-white uppercase tracking-wider mb-3">Subscribe</h3>
      <form class="space-y-2">
        <label for="footer-email-{idx}" class="sr-only">Work Email</label>
        <input id="footer-email-{idx}" type="email" placeholder="dev@company.com" required class="w-full px-3 py-2 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-white" />
        <button type="submit" class="w-full py-2 rounded-lg {pal['btn']} text-xs font-bold">Stay Updated</button>
      </form>
    </div>
  </div>
  <div class="max-w-7xl mx-auto px-6 mt-12 pt-6 border-t border-zinc-900 flex flex-col md:flex-row items-center justify-between text-xs text-zinc-600 gap-4">
    <p>&copy; 2026 Ornàment Engineering Platform. Open-source under MIT License.</p>
    <div class="flex space-x-6">
      <a href="/privacy" class="hover:text-zinc-400">Privacy Policy</a>
      <a href="/terms" class="hover:text-zinc-400">Terms of Service</a>
      <a href="/security" class="hover:text-zinc-400">Security Architecture</a>
    </div>
  </div>
</footer>"""

def _build_tables(idx: int, pal: Dict[str, str]) -> str:
    return f"""<section class="py-12 {pal['bg']} text-zinc-100">
  <div class="max-w-6xl mx-auto px-6">
    <div class="overflow-x-auto rounded-2xl {pal['card']} border border-zinc-800">
      <table class="w-full text-left text-xs">
        <caption class="p-5 font-bold text-sm text-white border-b border-zinc-800 text-left">
          Multi-Level Verification Harness Log • Commit #{idx + 100}
        </caption>
        <thead class="bg-zinc-950/60 uppercase font-mono text-zinc-400 border-b border-zinc-800">
          <tr>
            <th scope="col" class="py-3.5 px-6">Test Tier</th>
            <th scope="col" class="py-3.5 px-6">Target Component</th>
            <th scope="col" class="py-3.5 px-6">Execution Latency</th>
            <th scope="col" class="py-3.5 px-6">Status</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-zinc-800/60">
          <tr class="hover:bg-zinc-800/30 transition">
            <td class="py-3.5 px-6 font-semibold text-white">Level 1 Static Analysis</td>
            <td class="py-3.5 px-6 text-zinc-400">app/page.tsx, components/Navbar.tsx</td>
            <td class="py-3.5 px-6 font-mono text-zinc-400">12 ms</td>
            <td class="py-3.5 px-6"><span class="px-2.5 py-0.5 rounded-full bg-emerald-950 text-emerald-400 font-bold border border-emerald-800/60">[PASS]</span></td>
          </tr>
          <tr class="hover:bg-zinc-800/30 transition">
            <td class="py-3.5 px-6 font-semibold text-white">Level 4 Browser Functional</td>
            <td class="py-3.5 px-6 text-zinc-400">#nav-contact-button -> /contact route</td>
            <td class="py-3.5 px-6 font-mono text-zinc-400">114 ms</td>
            <td class="py-3.5 px-6"><span class="px-2.5 py-0.5 rounded-full bg-emerald-950 text-emerald-400 font-bold border border-emerald-800/60">[PASS]</span></td>
          </tr>
          <tr class="hover:bg-zinc-800/30 transition">
            <td class="py-3.5 px-6 font-semibold text-white">Level 7 WCAG A11y Audit</td>
            <td class="py-3.5 px-6 text-zinc-400">Color Contrast & Form Labels</td>
            <td class="py-3.5 px-6 font-mono text-zinc-400">45 ms</td>
            <td class="py-3.5 px-6"><span class="px-2.5 py-0.5 rounded-full bg-emerald-950 text-emerald-400 font-bold border border-emerald-800/60">[PASS]</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</section>"""

def _build_accessibility(idx: int, pal: Dict[str, str]) -> str:
    return f"""<section aria-labelledby="a11y-heading-{idx}" class="py-12 {pal['bg']} text-zinc-100">
  <div class="max-w-4xl mx-auto px-6 space-y-6">
    <a href="#main-content" class="sr-only focus:not-sr-only focus:p-3 focus:bg-indigo-600 focus:text-white rounded-lg">Skip to main content</a>
    <div class="p-8 rounded-2xl {pal['card']} space-y-4">
      <div class="flex items-center space-x-2 text-xs font-mono {pal['accent']}">
        <span class="w-2.5 h-2.5 rounded-full bg-current"></span>
        <span>WCAG 2.1 AAA High-Contrast Landmark</span>
      </div>
      <h2 id="a11y-heading-{idx}" class="text-2xl font-black text-white">Accessible Keyboard Navigation Module</h2>
      <p class="text-sm text-zinc-300 leading-relaxed">
        Engineered with explicit aria-live status regions, keyboard focus indicators (outline-offset-2), and high-contrast color ratios exceeding 7.0:1.
      </p>
      <div role="region" aria-live="polite" class="p-4 rounded-xl bg-zinc-950 border border-zinc-800 text-xs text-zinc-300">
        <span class="font-bold text-white">Screen Reader Announcement:</span> Active focus safely bounded in sandboxed DOM environment.
      </div>
      <div class="flex space-x-4 pt-2">
        <button class="px-5 py-2.5 rounded-xl {pal['btn']} text-xs font-bold focus:ring-2 focus:ring-white focus:outline-none">Accessible Action</button>
        <button class="px-5 py-2.5 rounded-xl bg-zinc-800 text-zinc-200 text-xs font-semibold hover:bg-zinc-700 focus:ring-2 focus:ring-white focus:outline-none">Dismiss Notice</button>
      </div>
    </div>
  </div>
</section>"""

def _build_buttons(idx: int, pal: Dict[str, str]) -> str:
    return f"""<section class="py-12 {pal['bg']} text-zinc-100">
  <div class="max-w-3xl mx-auto px-6 p-8 rounded-2xl {pal['card']} space-y-6">
    <h2 class="text-xl font-bold text-white">Interactive Button Component States</h2>
    <div class="flex flex-wrap items-center gap-4">
      <button type="button" class="px-5 py-2.5 rounded-xl {pal['btn']} text-xs font-bold shadow-md hover:scale-105 active:scale-95 transition">Primary Action</button>
      <button type="button" class="px-5 py-2.5 rounded-xl bg-zinc-800 text-zinc-200 text-xs font-semibold hover:bg-zinc-700 active:scale-95 transition">Secondary Action</button>
      <button type="button" class="px-5 py-2.5 rounded-xl bg-rose-600/20 text-rose-300 border border-rose-600/40 text-xs font-semibold hover:bg-rose-600/30 transition">Destructive Rollback</button>
      <button type="button" disabled class="px-5 py-2.5 rounded-xl bg-zinc-900 text-zinc-600 cursor-not-allowed text-xs font-medium border border-zinc-800">Disabled State</button>
    </div>
  </div>
</section>"""

def generate_html(count: int, categories: List[str] = None) -> List[Dict[str, Any]]:
    """
    Generates 'count' high-quality, production-grade HTML examples across categories.
    """
    if not categories:
        categories = ["heroes", "cards", "pricing", "forms", "portfolios", "complete_pages", "dashboards", "ecommerce", "footers", "tables", "accessibility", "buttons"]

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
        elif cat in ["pricing"]:
            code = _build_pricing(i, pal)
            desc = f"Tiered pricing matrix with recommended badges and {pal['name']} theme"
        elif cat in ["forms", "contact"]:
            code = _build_form(i, pal)
            desc = f"Accessible contact request form with validation styling"
        elif cat in ["dashboards"]:
            code = _build_dashboard(i, pal)
            desc = f"Bento metric telemetry dashboard in {pal['name']} style"
        elif cat in ["ecommerce"]:
            code = _build_ecommerce(i, pal)
            desc = f"Hardware e-commerce product showcase grid with {pal['name']} theme"
        elif cat in ["footers"]:
            code = _build_footer(i, pal)
            desc = f"Comprehensive 4-column footer with newsletter and legal navigation"
        elif cat in ["tables"]:
            code = _build_tables(i, pal)
            desc = f"Accessible data table with scope attributes and zebra striping"
        elif cat in ["accessibility"]:
            code = _build_accessibility(i, pal)
            desc = f"High-contrast WCAG 2.1 AAA accessible component with aria-live"
        elif cat in ["buttons"]:
            code = _build_buttons(i, pal)
            desc = f"Interactive button state gallery with primary, secondary, and disabled styles"
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
