"""
Web Design Intelligence & Practical Code Generator for Ornàment.
Generates comprehensive instruction-response training pairs covering:
1. Color Psychology & OKLCH/HSL Palette Engineering
2. Customer Psychology & UX Interaction Laws (Hick's, Fitts's, Doherty <400ms)
3. Business Strategy & Conversion Architecture (Proof Stacking, Product-as-Demo)
4. UI/UX Design Systems (Bento grids, 8pt spatial grid, Perfect Fourth typography)
5. Production-Ready Practical Code Implementations
"""

from typing import List, Dict, Any

INTELLIGENCE_PAIRS: List[Dict[str, Any]] = [
    {
        "category": "conversion_hero_architecture",
        "instruction": (
            "Design and code a high-converting 2026 SaaS Hero Section applying Hick's Law (One Primary CTA), "
            "Fitts's Law (48px+ touch target), Proof Stacking, and the modern 'Product-as-Demo' paradigm. "
            "Use dark luxury aesthetics (60-30-10 palette) with Tailwind CSS."
        ),
        "input": "",
        "output": (
            "### High-Converting 2026 SaaS Hero: Architectural Rationale\n\n"
            "1. **Hick's Law (Friction Minimization)**: Exactly one primary high-contrast CTA above the fold, preventing choice overload.\n"
            "2. **Fitts's Law (Target Accessibility)**: Primary button has 48px height (`py-3.5 px-7`) with generous cursor hit-zone and spring active state.\n"
            "3. **Proof Stacking**: Enterprise trust badges and live metric pill ('Trusted by 12,000+ engineers') positioned directly under the headline.\n"
            "4. **Product-as-Demo**: Instead of a flat static screenshot, the hero features a live interactive telemetry card simulating real AI performance.\n"
            "5. **60-30-10 Palette**: 60% Canvas (`bg-zinc-950`), 30% Elevated Surface (`bg-zinc-900/50 border border-white/10`), 10% Electric Indigo accent.\n\n"
            "```html\n"
            "<header class=\"relative w-full overflow-hidden bg-zinc-950 text-zinc-100 pt-20 pb-24 border-b border-zinc-900\">\n"
            "  <!-- Ambient Radial Glow -->\n"
            "  <div class=\"absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-indigo-500/10 rounded-full blur-[120px] pointer-events-none\" aria-hidden=\"true\"></div>\n"
            "\n"
            "  <div class=\"relative max-w-7xl mx-auto px-6 lg:px-8 flex flex-col items-center text-center space-y-8\">\n"
            "    <!-- Proof Pill -->\n"
            "    <div class=\"inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-zinc-900/80 border border-zinc-800 text-xs text-zinc-300 font-mono shadow-sm\">\n"
            "      <span class=\"w-2 h-2 rounded-full bg-emerald-400 animate-pulse\"></span>\n"
            "      <span>Trusted by 12,400+ Autonomous Teams • 99.99% Reliability</span>\n"
            "    </div>\n"
            "\n"
            "    <!-- Headline: Clarifies What, For Whom, and Why in 5 Seconds -->\n"
            "    <h1 class=\"max-w-4xl text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-[1.1]\">\n"
            "      Autonomous Website Engineering <br class=\"hidden sm:inline\" />\n"
            "      <span class=\"text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-indigo-200 to-white\">\n"
            "        Powered by Local Intelligence.\n"
            "      </span>\n"
            "    </h1>\n"
            "\n"
            "    <!-- Supporting Value Proposition -->\n"
            "    <p class=\"max-w-2xl text-lg sm:text-xl text-zinc-400 font-normal leading-relaxed\">\n"
            "      Ornàment inspects, synthesizes, and repairs production-grade websites under strict minimal change policies—running 100% offline on your machine.\n"
            "    </p>\n"
            "\n"
            "    <!-- Hick's Law: Single High-Contrast Primary CTA -->\n"
            "    <div class=\"flex flex-col sm:flex-row items-center gap-4 pt-2\">\n"
            "      <a href=\"#deploy\"\n"
            "         class=\"w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl\n"
            "                bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm\n"
            "                shadow-[0_0_24px_rgba(99,102,241,0.4),inset_0_1px_0_0_rgba(255,255,255,0.2)]\n"
            "                active:scale-[0.98] transition-all duration-200 ease-[cubic-bezier(0.16,1,0.3,1)]\n"
            "                focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:ring-offset-2 focus-visible:ring-offset-zinc-950\">\n"
            "        <span>Deploy Local Engineer</span>\n"
            "        <svg class=\"w-4 h-4\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M13 7l5 5m0 0l-5 5m5-5H6\"/></svg>\n"
            "      </a>\n"
            "      <span class=\"text-xs text-zinc-500 font-mono\">Zero cloud API • Instant GGUF GPU inference</span>\n"
            "    </div>\n"
            "\n"
            "    <!-- Product-as-Demo: Live Telemetry Card -->\n"
            "    <div class=\"w-full max-w-4xl mt-12 p-6 rounded-2xl bg-zinc-900/60 border border-zinc-800/80 shadow-2xl backdrop-blur-xl text-left\">\n"
            "      <div class=\"flex items-center justify-between pb-4 border-b border-zinc-800 text-xs font-mono text-zinc-400\">\n"
            "        <div class=\"flex items-center gap-2\">\n"
            "          <span class=\"w-3 h-3 rounded-full bg-rose-500/80\"></span>\n"
            "          <span class=\"w-3 h-3 rounded-full bg-amber-500/80\"></span>\n"
            "          <span class=\"w-3 h-3 rounded-full bg-emerald-500/80\"></span>\n"
            "          <span class=\"ml-2 text-zinc-300 font-bold\">ornament-agent.local:5050</span>\n"
            "        </div>\n"
            "        <span class=\"text-emerald-400 font-semibold\">RTX 3050 GPU • 4.1GB VRAM</span>\n"
            "      </div>\n"
            "      <div class=\"grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 text-xs\">\n"
            "        <div class=\"p-3 rounded-lg bg-zinc-950/60 border border-zinc-800/50\">\n"
            "          <div class=\"text-zinc-500\">Architecture</div>\n"
            "          <div class=\"font-bold text-white mt-1\">Qwen2.5-Coder-3B QLoRA</div>\n"
            "        </div>\n"
            "        <div class=\"p-3 rounded-lg bg-zinc-950/60 border border-zinc-800/50\">\n"
            "          <div class=\"text-zinc-500\">Surgical Repair Policy</div>\n"
            "          <div class=\"font-bold text-emerald-400 mt-1\">1-File Minimal Diff [Active]</div>\n"
            "        </div>\n"
            "        <div class=\"p-3 rounded-lg bg-zinc-950/60 border border-zinc-800/50\">\n"
            "          <div class=\"text-zinc-500\">Test Pass Rate</div>\n"
            "          <div class=\"font-bold text-indigo-400 mt-1\">100% Playwright DOM Verified</div>\n"
            "        </div>\n"
            "      </div>\n"
            "    </div>\n"
            "  </div>\n"
            "</header>\n"
            "```"
        ),
        "metadata": {"category": "conversion_hero", "difficulty": "expert", "tokens": 680}
    },
    {
        "category": "bento_grid_psychology",
        "instruction": (
            "Explain how the Bento Grid layout solves cognitive information density in modern UI/UX design. "
            "Write a production-ready HTML5 + Tailwind Bento Grid featuring 3 asymmetrical cards with hover glows "
            "and Doherty Threshold (<400ms) micro-interactions."
        ),
        "input": "",
        "output": (
            "### The Bento Grid: Solving Cognitive Load and Visual Hierarchy\n\n"
            "The Bento Grid layout, inspired by Japanese bento boxes, organizes complex, heterogeneous information into compartmentalized visual cells. "
            "Rather than forcing repetitive identical cards, an asymmetrical Bento grid directs user eye movement by allocating a 2-column span to the **flagship capability**, "
            "while secondary cells handle metrics and social proof. This honors **Miller's Law (7±2 chunks)** by packaging disparate features into easily digestible cognitive containers.\n\n"
            "```html\n"
            "<section class=\"py-20 bg-zinc-950 text-zinc-100\">\n"
            "  <div class=\"max-w-7xl mx-auto px-6\">\n"
            "    <div class=\"mb-12 text-center\">\n"
            "      <h2 class=\"text-3xl sm:text-4xl font-bold tracking-tight text-white\">Engineered for Pure Performance</h2>\n"
            "      <p class=\"mt-3 text-zinc-400 text-base\">Every subsystem tuned for sub-400ms latency and minimal cognitive friction.</p>\n"
            "    </div>\n"
            "\n"
            "    <!-- Bento Grid Container -->\n"
            "    <div class=\"grid grid-cols-1 md:grid-cols-3 gap-6\">\n"
            "      <!-- Primary Flagship Cell (Spans 2 columns) -->\n"
            "      <article class=\"group relative md:col-span-2 p-8 rounded-3xl bg-zinc-900/40 border border-zinc-800/80 hover:border-zinc-700/80 transition-all duration-300 overflow-hidden backdrop-blur-xl\">\n"
            "        <div class=\"absolute -top-20 -right-20 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl group-hover:bg-indigo-500/20 transition-all duration-500 pointer-events-none\"></div>\n"
            "        <span class=\"text-xs font-mono font-semibold text-indigo-400 uppercase tracking-wider\">Flagship Subsystem</span>\n"
            "        <h3 class=\"text-2xl font-bold text-white mt-3\">Autonomous Multi-Agent Fleet</h3>\n"
            "        <p class=\"text-zinc-400 text-sm mt-2 max-w-lg leading-relaxed\">\n"
            "          Architect, Code, and Test agents collaborate in real-time. Code is checked against Playwright DOM tests and repaired automatically before you ever hit save.\n"
            "        </p>\n"
            "        <div class=\"mt-6 p-4 rounded-xl bg-zinc-950/80 border border-zinc-800 font-mono text-xs text-zinc-300 space-y-1\">\n"
            "          <div class=\"text-emerald-400\">✓ Architect Agent [SPEC APPROVED]</div>\n"
            "          <div class=\"text-indigo-400\">✓ Code Agent [SYNTHESIZED 12 COMPONENTS]</div>\n"
            "          <div class=\"text-zinc-400\">✓ Test Agent [PLAYWRIGHT DOM 100% PASS]</div>\n"
            "        </div>\n"
            "      </article>\n"
            "\n"
            "      <!-- Secondary Cell: Live Telemetry Metric -->\n"
            "      <article class=\"group relative p-8 rounded-3xl bg-zinc-900/40 border border-zinc-800/80 hover:border-zinc-700/80 transition-all duration-300 flex flex-col justify-between backdrop-blur-xl\">\n"
            "        <div>\n"
            "          <span class=\"text-xs font-mono font-semibold text-emerald-400 uppercase tracking-wider\">Response Speed</span>\n"
            "          <h3 class=\"text-4xl font-extrabold text-white mt-3\">32ms</h3>\n"
            "          <p class=\"text-zinc-400 text-xs mt-2\">Instant sub-400ms Doherty threshold feedback on every local LLM invocation.</p>\n"
            "        </div>\n"
            "        <div class=\"mt-6 pt-4 border-t border-zinc-800/60 flex items-center justify-between text-xs text-zinc-500 font-mono\">\n"
            "          <span>Status: Optimal</span>\n"
            "          <span class=\"w-2 h-2 rounded-full bg-emerald-400 animate-ping\"></span>\n"
            "        </div>\n"
            "      </article>\n"
            "    </div>\n"
            "  </div>\n"
            "</section>\n"
            "```"
        ),
        "metadata": {"category": "bento_grid", "difficulty": "expert", "tokens": 620}
    },
    {
        "category": "pricing_psychology",
        "instruction": (
            "Explain the behavioral psychology of a 3-Tier SaaS Pricing Table (Decoy Effect, Loss Aversion, Default Bias). "
            "Write the HTML5 + Tailwind CSS implementation with an elevated 'Most Popular' card."
        ),
        "input": "",
        "output": (
            "### Behavioral Psychology of 3-Tier SaaS Pricing\n\n"
            "1. **Decoy Effect (Asymmetric Dominance)**: The Starter tier anchors value, the Enterprise tier sets an aspirational ceiling, making the middle **Pro Tier** appear overwhelmingly superior in cost-per-feature ratio.\n"
            "2. **Default Bias (Social Proof Anchor)**: Highlighting the center tier with an elevated border, badge ('Most Popular'), and subtle glow triggers the cognitive heuristic that 'most people chose this, so it must be safe'.\n"
            "3. **Loss Aversion**: Framing features around what users *prevent losing* ('Never lose working code with Git checkpoints') rather than vague abstractions.\n\n"
            "```html\n"
            "<section class=\"py-20 bg-zinc-950 text-zinc-100\">\n"
            "  <div class=\"max-w-7xl mx-auto px-6\">\n"
            "    <div class=\"text-center max-w-2xl mx-auto mb-16\">\n"
            "      <h2 class=\"text-3xl font-extrabold text-white sm:text-4xl\">Predictable Pricing. Zero Subscriptions.</h2>\n"
            "      <p class=\"mt-3 text-zinc-400 text-sm\">Deploy locally on your hardware. You own 100% of your code and models forever.</p>\n"
            "    </div>\n"
            "\n"
            "    <div class=\"grid grid-cols-1 md:grid-cols-3 gap-8 items-center\">\n"
            "      <!-- Starter Tier -->\n"
            "      <div class=\"p-8 rounded-2xl bg-zinc-900/30 border border-zinc-800 text-zinc-300 space-y-6\">\n"
            "        <div>\n"
            "          <h3 class=\"text-lg font-bold text-white\">Community</h3>\n"
            "          <div class=\"mt-3 text-3xl font-extrabold text-white\">$0 <span class=\"text-xs font-normal text-zinc-500\">forever</span></div>\n"
            "          <p class=\"text-xs text-zinc-400 mt-2\">For developers building personal portfolios and learning web engineering.</p>\n"
            "        </div>\n"
            "        <ul class=\"space-y-3 text-xs\">\n"
            "          <li class=\"flex items-center gap-2\">✓ Local GGUF Inference</li>\n"
            "          <li class=\"flex items-center gap-2\">✓ Semantic HTML5 Scaffolding</li>\n"
            "          <li class=\"flex items-center gap-2 text-zinc-500\">✗ Multi-Agent Repair Loop</li>\n"
            "        </ul>\n"
            "        <button class=\"w-full py-2.5 rounded-xl border border-zinc-700 bg-zinc-900 text-xs font-bold hover:bg-zinc-800 transition\">Download Free</button>\n"
            "      </div>\n"
            "\n"
            "      <!-- Pro Tier (Elevated 'Most Popular' Center) -->\n"
            "      <div class=\"relative p-8 rounded-3xl bg-zinc-900/80 border-2 border-indigo-500 shadow-[0_0_36px_rgba(99,102,241,0.25)] text-white space-y-6 md:-translate-y-2\">\n"
            "        <div class=\"absolute -top-3.5 left-1/2 -translate-x-1/2 px-3.5 py-1 rounded-full bg-indigo-600 text-[10px] font-mono font-bold uppercase tracking-wider shadow\">\n"
            "          Most Popular\n"
            "        </div>\n"
            "        <div>\n"
            "          <h3 class=\"text-xl font-bold\">Engineer Pro</h3>\n"
            "          <div class=\"mt-3 text-4xl font-extrabold\">$49 <span class=\"text-xs font-normal text-zinc-400\">one-time</span></div>\n"
            "          <p class=\"text-xs text-zinc-300 mt-2\">Complete autonomous fleet with self-diagnosing minimal change loops.</p>\n"
            "        </div>\n"
            "        <ul class=\"space-y-3 text-xs\">\n"
            "          <li class=\"flex items-center gap-2\"><span class=\"text-indigo-400 font-bold\">✓</span> Autonomous Playwright Repair Loop</li>\n"
            "          <li class=\"flex items-center gap-2\"><span class=\"text-indigo-400 font-bold\">✓</span> 4-bit QLoRA Custom Fine-Tuning</li>\n"
            "          <li class=\"flex items-center gap-2\"><span class=\"text-indigo-400 font-bold\">✓</span> Unlimited Local Projects & Checkpoints</li>\n"
            "        </ul>\n"
            "        <button class=\"w-full py-3.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-xs font-bold shadow-lg transition active:scale-[0.98]\">\n"
            "          Get Lifetime Access\n"
            "        </button>\n"
            "      </div>\n"
            "\n"
            "      <!-- Enterprise Tier -->\n"
            "      <div class=\"p-8 rounded-2xl bg-zinc-900/30 border border-zinc-800 text-zinc-300 space-y-6\">\n"
            "        <div>\n"
            "          <h3 class=\"text-lg font-bold text-white\">Studio Team</h3>\n"
            "          <div class=\"mt-3 text-3xl font-extrabold text-white\">$199 <span class=\"text-xs font-normal text-zinc-500\">one-time</span></div>\n"
            "          <p class=\"text-xs text-zinc-400 mt-2\">For agencies building high-velocity client sites with custom design tokens.</p>\n"
            "        </div>\n"
            "        <ul class=\"space-y-3 text-xs\">\n"
            "          <li class=\"flex items-center gap-2\">✓ Multi-GPU Server Cluster</li>\n"
            "          <li class=\"flex items-center gap-2\">✓ Custom Design System Ingestion</li>\n"
            "          <li class=\"flex items-center gap-2\">✓ Priority Engineering Support</li>\n"
            "        </ul>\n"
            "        <button class=\"w-full py-2.5 rounded-xl border border-zinc-700 bg-zinc-900 text-xs font-bold hover:bg-zinc-800 transition\">Deploy Studio</button>\n"
            "      </div>\n"
            "    </div>\n"
            "  </div>\n"
            "</section>\n"
            "```"
        ),
        "metadata": {"category": "pricing_psychology", "difficulty": "expert", "tokens": 710}
    }
]

class WebDesignIntelligenceGenerator:
    """Generates web design intelligence and conversion architecture training pairs."""

    @classmethod
    def generate(cls) -> List[Dict[str, Any]]:
        results = []
        for i, pair in enumerate(INTELLIGENCE_PAIRS, 1):
            results.append({
                "id": f"intel_{i:06d}",
                "instruction": pair["instruction"],
                "input": pair.get("input", ""),
                "output": pair["output"],
                "metadata": pair.get("metadata", {})
            })
        return results
