from pathlib import Path
from typing import Dict, Any, List
from ornament.files.file_manager import FileManager

class CustomSiteGenerator:
    """
    Generates high-fidelity websites customized by user prompt, site category,
    aesthetic style, color palette, and selected sections.
    Outputs both modular Next.js components and a live standalone preview.
    """

    PALETTE_MAP = {
        "indigo": {
            "primary": "#6366f1",
            "primary_hover": "#4f46e5",
            "primary_text": "text-indigo-400",
            "primary_bg": "bg-indigo-600",
            "primary_border": "border-indigo-500/30",
            "glow": "rgba(99, 102, 241, 0.25)"
        },
        "emerald": {
            "primary": "#10b981",
            "primary_hover": "#059669",
            "primary_text": "text-emerald-400",
            "primary_bg": "bg-emerald-600",
            "primary_border": "border-emerald-500/30",
            "glow": "rgba(16, 185, 129, 0.25)"
        },
        "cyan": {
            "primary": "#06b6d4",
            "primary_hover": "#0891b2",
            "primary_text": "text-cyan-400",
            "primary_bg": "bg-cyan-600",
            "primary_border": "border-cyan-500/30",
            "glow": "rgba(6, 182, 212, 0.25)"
        },
        "amber": {
            "primary": "#f59e0b",
            "primary_hover": "#d97706",
            "primary_text": "text-amber-400",
            "primary_bg": "bg-amber-600",
            "primary_border": "border-amber-500/30",
            "glow": "rgba(245, 158, 11, 0.25)"
        },
        "violet": {
            "primary": "#8b5cf6",
            "primary_hover": "#7c3aed",
            "primary_text": "text-violet-400",
            "primary_bg": "bg-violet-600",
            "primary_border": "border-violet-500/30",
            "glow": "rgba(139, 92, 246, 0.25)"
        }
    }

    @classmethod
    def generate(
        cls,
        workspace_path: Path,
        prompt: str,
        site_type: str = "portfolio",
        style: str = "dark_futuristic",
        palette_key: str = "indigo",
        sections: List[str] = None
    ) -> Dict[str, Any]:
        fm = FileManager(workspace_path)
        palette = cls.PALETTE_MAP.get(palette_key.lower(), cls.PALETTE_MAP["indigo"])
        if not sections:
            sections = ["hero", "features", "stats", "pricing", "contact"]

        title = prompt.strip().split(".")[0] if prompt.strip() else f"Modern {site_type.capitalize()}"
        if len(title) > 60:
            title = title[:60] + "..."

        # Generate public/preview.html for instant live rendering in iframe
        preview_html = cls._build_preview_html(
            title=title,
            prompt=prompt,
            site_type=site_type,
            style=style,
            palette=palette,
            sections=sections
        )
        fm.create_file("public/preview.html", preview_html, overwrite=True)

        # Generate Next.js App Router code
        # 1. package.json
        package_json = """{
  "name": "ornament-custom-site",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^14.2.3",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "lucide-react": "^0.378.0"
  },
  "devDependencies": {
    "@types/node": "^20.12.7",
    "@types/react": "^18.3.1",
    "@types/react-dom": "^18.3.1",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.3",
    "typescript": "^5.4.5"
  }
}
"""
        fm.create_file("package.json", package_json, overwrite=True)

        # 2. tailwind.config.js
        tailwind_config = f"""/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  content: [
    "./app/**/*.{{js,ts,jsx,tsx,mdx}}",
    "./components/**/*.{{js,ts,jsx,tsx,mdx}}",
  ],
  darkMode: "class",
  theme: {{
    extend: {{
      colors: {{
        background: "#09090b",
        surface: "#18181b",
        border: "#27272a",
        accent: "{palette['primary']}"
      }}
    }},
  }},
  plugins: [],
}}
"""
        fm.create_file("tailwind.config.js", tailwind_config, overwrite=True)

        # 3. app/globals.css
        globals_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  color-scheme: dark;
}

body {
  background-color: #09090b;
  color: #f4f4f5;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
"""
        fm.create_file("app/globals.css", globals_css, overwrite=True)

        # 4. app/layout.tsx
        layout_tsx = f"""import "./globals.css";
import React from "react";
import Navbar from "@/components/Navbar";

export const metadata = {{
  title: "{title}",
  description: "{prompt[:100] if prompt else 'High-performance autonomous website.'}",
}};

export default function RootLayout({{
  children,
}}: {{
  children: React.ReactNode;
}}) {{
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen flex flex-col bg-background text-zinc-100 antialiased">
        <Navbar />
        <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {{children}}
        </main>
      </body>
    </html>
  );
}}
"""
        fm.create_file("app/layout.tsx", layout_tsx, overwrite=True)

        # 5. components/Navbar.tsx
        navbar_code = f"""import React from "react";

export default function Navbar() {{
  return (
    <header className="sticky top-0 z-50 w-full border-b border-zinc-800 bg-zinc-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg {palette['primary_bg']} flex items-center justify-center font-black text-white">
            {site_type[0].upper()}
          </div>
          <span className="font-bold text-lg text-white tracking-tight">{site_type.capitalize()}<span className="{palette['primary_text']}">.ai</span></span>
        </div>
        <nav aria-label="Main Navigation" className="hidden md:flex items-center space-x-6 text-sm">
          <a href="#features" className="text-zinc-400 hover:text-white transition">Features</a>
          <a href="#stats" className="text-zinc-400 hover:text-white transition">Metrics</a>
          <a href="#pricing" className="text-zinc-400 hover:text-white transition">Pricing</a>
          <a id="nav-contact-button" href="/contact" className="px-4 py-2 rounded-full {palette['primary_bg']} hover:opacity-90 text-white font-medium transition shadow-lg">
            Get Started
          </a>
        </nav>
      </div>
    </header>
  );
}}
"""
        fm.create_file("components/Navbar.tsx", navbar_code, overwrite=True)

        # 3. app/page.tsx
        page_code = f"""import React from "react";
import Navbar from "@/components/Navbar";

export default function HomePage() {{
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 font-sans selection:bg-indigo-500 selection:text-white">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-24">
        {{/* Hero Section */}}
        <section className="text-center py-12 max-w-4xl mx-auto space-y-6">
          <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-zinc-900 border {palette['primary_border']} {palette['primary_text']}">
            {style.replace("_", " ").title()} • {site_type.upper()}
          </div>
          <h1 className="text-5xl md:text-6xl font-black text-white tracking-tight leading-tight">
            {title}
          </h1>
          <p className="text-lg text-zinc-400 max-w-2xl mx-auto leading-relaxed">
            {prompt if prompt else "Engineered with autonomous precision, high-conversion typography, and responsive modern architecture."}
          </p>
          <div className="flex items-center justify-center space-x-4 pt-4">
            <a href="/contact" className="px-6 py-3 rounded-xl {palette['primary_bg']} text-white font-bold hover:opacity-90 shadow-xl transition">
              Explore Platform
            </a>
            <a href="#features" className="px-6 py-3 rounded-xl bg-zinc-900 hover:bg-zinc-800 text-zinc-300 font-semibold border border-zinc-800 transition">
              Documentation
            </a>
          </div>
        </section>
      </main>
    </div>
  );
}}
"""
        fm.create_file("app/page.tsx", page_code, overwrite=True)

        # 4. app/contact/page.tsx
        contact_code = f"""import React from "react";
import Navbar from "@/components/Navbar";

export default function ContactPage() {{
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <Navbar />
      <main className="max-w-2xl mx-auto px-4 py-16">
        <h1 className="text-3xl font-extrabold text-white mb-2">Connect with Engineering</h1>
        <p className="text-sm text-zinc-400 mb-8">Direct line to the autonomous Ornàment engineering system.</p>
        <form className="space-y-4 bg-zinc-900 p-8 rounded-2xl border border-zinc-800">
          <div>
            <label className="block text-xs font-semibold text-zinc-400 mb-1">Name</label>
            <input aria-label="Your Name" className="w-full p-3 rounded-lg bg-zinc-800 border border-zinc-700 text-white" />
          </div>
          <div>
            <label className="block text-xs font-semibold text-zinc-400 mb-1">Email</label>
            <input type="email" aria-label="Email" className="w-full p-3 rounded-lg bg-zinc-800 border border-zinc-700 text-white" />
          </div>
          <div>
            <label className="block text-xs font-semibold text-zinc-400 mb-1">Message</label>
            <textarea rows={4} aria-label="Message" className="w-full p-3 rounded-lg bg-zinc-800 border border-zinc-700 text-white"></textarea>
          </div>
          <button type="button" className="w-full py-3 rounded-lg {palette['primary_bg']} text-white font-bold hover:opacity-90 shadow-lg">
            Submit Request
          </button>
        </form>
      </main>
    </div>
  );
}}
"""
        fm.create_file("app/contact/page.tsx", contact_code, overwrite=True)

        return {
            "status": "generated",
            "site_type": site_type,
            "title": title,
            "files_count": len(fm.list_files(exclude_build=True)),
            "preview_file": "public/preview.html"
        }

    @classmethod
    def _build_preview_html(
        cls,
        title: str,
        prompt: str,
        site_type: str,
        style: str,
        palette: Dict[str, str],
        sections: List[str]
    ) -> str:
        prompt_text = prompt if prompt else f"Modern, high-performance {site_type} with responsive layout, semantic markup, and accessible components."

        # Hero section
        hero_html = f"""
    <!-- HERO SECTION -->
    <section class="py-20 text-center relative overflow-hidden border-b border-zinc-800/80">
      <div class="absolute inset-0 bg-gradient-to-b from-[{palette['glow']}] to-transparent opacity-30 pointer-events-none"></div>
      <div class="max-w-4xl mx-auto px-4 relative z-10 space-y-6">
        <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-semibold bg-zinc-900 border {palette['primary_border']} {palette['primary_text']}">
          <span class="w-2 h-2 rounded-full {palette['primary_bg']} animate-ping"></span>
          <span>{style.replace('_', ' ').title()} Edition</span>
        </div>
        <h1 class="text-4xl sm:text-6xl font-black text-white tracking-tight leading-tight">
          {title}
        </h1>
        <p class="text-base sm:text-lg text-zinc-400 max-w-2xl mx-auto leading-relaxed">
          {prompt_text}
        </p>
        <div class="flex flex-wrap items-center justify-center gap-4 pt-4">
          <a id="nav-contact-button" href="/contact" class="px-6 py-3.5 rounded-xl {palette['primary_bg']} hover:opacity-95 text-white font-bold text-sm shadow-xl shadow-[{palette['glow']}] transition transform hover:-translate-y-0.5">
            Get Started Now
          </a>
          <a href="#features" class="px-6 py-3.5 rounded-xl bg-zinc-900 hover:bg-zinc-800 text-zinc-300 font-semibold text-sm border border-zinc-800 transition">
            View Architecture
          </a>
        </div>
      </div>
    </section>
"""

        # Features / Bento Grid
        features_html = ""
        if "features" in sections:
            features_html = f"""
    <!-- BENTO GRID FEATURES -->
    <section id="features" class="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <h2 class="text-xs uppercase font-bold tracking-widest {palette['primary_text']} mb-2">Engineered Capabilities</h2>
        <h3 class="text-3xl font-extrabold text-white">Built for High Reliability & Scale</h3>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="p-8 rounded-2xl bg-zinc-900/60 border border-zinc-800/80 hover:border-zinc-700 transition">
          <div class="w-12 h-12 rounded-xl {palette['primary_bg']} bg-opacity-10 {palette['primary_text']} flex items-center justify-center font-bold text-lg mb-6">01</div>
          <h4 class="text-xl font-bold text-white mb-2">Minimal Change Patching</h4>
          <p class="text-sm text-zinc-400 leading-relaxed">Surgically isolates root causes and writes targeted 1-file diffs without wiping or regenerating entire codebases.</p>
        </div>
        <div class="p-8 rounded-2xl bg-zinc-900/60 border border-zinc-800/80 hover:border-zinc-700 transition">
          <div class="w-12 h-12 rounded-xl {palette['primary_bg']} bg-opacity-10 {palette['primary_text']} flex items-center justify-center font-bold text-lg mb-6">02</div>
          <h4 class="text-xl font-bold text-white mb-2">Automated Playwright Tests</h4>
          <p class="text-sm text-zinc-400 leading-relaxed">Continuous DOM assertion, navigation route checking, and accessibility auditing for production readiness.</p>
        </div>
        <div class="p-8 rounded-2xl bg-zinc-900/60 border border-zinc-800/80 hover:border-zinc-700 transition">
          <div class="w-12 h-12 rounded-xl {palette['primary_bg']} bg-opacity-10 {palette['primary_text']} flex items-center justify-center font-bold text-lg mb-6">03</div>
          <h4 class="text-xl font-bold text-white mb-2">Hardware-Gated Execution</h4>
          <p class="text-sm text-zinc-400 leading-relaxed">Monitors GPU VRAM and system memory in real time to throttle subagent concurrency and prevent thrashing.</p>
        </div>
      </div>
    </section>
"""

        # Stats section
        stats_html = ""
        if "stats" in sections:
            stats_html = f"""
    <!-- METRICS & TELEMETRY -->
    <section id="stats" class="py-16 bg-zinc-900/40 border-y border-zinc-800/80">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div>
            <div class="text-4xl font-black text-white font-mono">99.8%</div>
            <div class="text-xs text-zinc-400 uppercase tracking-wider mt-1">Autonomous Pass Rate</div>
          </div>
          <div>
            <div class="text-4xl font-black {palette['primary_text']} font-mono">&lt; 2.1s</div>
            <div class="text-xs text-zinc-400 uppercase tracking-wider mt-1">Diagnosis Latency</div>
          </div>
          <div>
            <div class="text-4xl font-black text-white font-mono">100 / 100</div>
            <div class="text-xs text-zinc-400 uppercase tracking-wider mt-1">Lighthouse A11y</div>
          </div>
          <div>
            <div class="text-4xl font-black {palette['primary_text']} font-mono">Zero</div>
            <div class="text-xs text-zinc-400 uppercase tracking-wider mt-1">Unhandled Regressions</div>
          </div>
        </div>
      </div>
    </section>
"""

        # Pricing section
        pricing_html = ""
        if "pricing" in sections:
            pricing_html = f"""
    <!-- PRICING TIERS -->
    <section id="pricing" class="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <h2 class="text-xs uppercase font-bold tracking-widest {palette['primary_text']} mb-2">Transparent Pricing</h2>
        <h3 class="text-3xl font-extrabold text-white">Deploy Locally or Scale to Fleet</h3>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="p-8 rounded-2xl bg-zinc-900/40 border border-zinc-800 flex flex-col justify-between">
          <div>
            <h4 class="font-bold text-white text-lg">Developer Local</h4>
            <div class="text-3xl font-black text-white mt-4">$0 <span class="text-sm font-normal text-zinc-400">/ forever</span></div>
            <p class="text-xs text-zinc-400 mt-2">Single-developer local installation on laptop RTX 3050 GPU.</p>
            <ul class="mt-6 space-y-3 text-xs text-zinc-300">
              <li class="flex items-center space-x-2"><span>[OK]</span><span>Local GGUF 4-bit inference</span></li>
              <li class="flex items-center space-x-2"><span>[OK]</span><span>Git Checkpoint rollbacks</span></li>
              <li class="flex items-center space-x-2"><span>[OK]</span><span>Playwright Level 1-7 testing</span></li>
            </ul>
          </div>
          <button class="mt-8 w-full py-2.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-white font-semibold text-xs border border-zinc-700">Current Plan</button>
        </div>
        <div class="p-8 rounded-2xl bg-zinc-900 border-2 {palette['primary_border']} relative flex flex-col justify-between shadow-2xl">
          <div class="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full {palette['primary_bg']} text-white text-[10px] font-bold uppercase tracking-wider">Most Popular</div>
          <div>
            <h4 class="font-bold text-white text-lg">Pro Engineer</h4>
            <div class="text-3xl font-black text-white mt-4">$49 <span class="text-sm font-normal text-zinc-400">/ month</span></div>
            <p class="text-xs text-zinc-400 mt-2">Unlimited autonomous repair loops with cloud training offload.</p>
            <ul class="mt-6 space-y-3 text-xs text-zinc-300">
              <li class="flex items-center space-x-2"><span class="{palette['primary_text']}">[OK]</span><span>Multi-agent hierarchy (Debug + Code + Test)</span></li>
              <li class="flex items-center space-x-2"><span class="{palette['primary_text']}">[OK]</span><span>Continuous Playwright browser validation</span></li>
              <li class="flex items-center space-x-2"><span class="{palette['primary_text']}">[OK]</span><span>Fine-tuned Qwen LoRA adapter updates</span></li>
            </ul>
          </div>
          <button class="mt-8 w-full py-2.5 rounded-lg {palette['primary_bg']} hover:opacity-90 text-white font-bold text-xs shadow-lg">Upgrade to Pro</button>
        </div>
        <div class="p-8 rounded-2xl bg-zinc-900/40 border border-zinc-800 flex flex-col justify-between">
          <div>
            <h4 class="font-bold text-white text-lg">Enterprise Fleet</h4>
            <div class="text-3xl font-black text-white mt-4">$299 <span class="text-sm font-normal text-zinc-400">/ month</span></div>
            <p class="text-xs text-zinc-400 mt-2">Distributed agent clusters with SLA and dedicated support.</p>
            <ul class="mt-6 space-y-3 text-xs text-zinc-300">
              <li class="flex items-center space-x-2"><span>[OK]</span><span>Full CI/CD pipeline integration</span></li>
              <li class="flex items-center space-x-2"><span>[OK]</span><span>Air-gapped on-premise deployment</span></li>
              <li class="flex items-center space-x-2"><span>[OK]</span><span>Custom design system fine-tuning</span></li>
            </ul>
          </div>
          <button class="mt-8 w-full py-2.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-white font-semibold text-xs border border-zinc-700">Contact Sales</button>
        </div>
      </div>
    </section>
"""

        # Contact section
        contact_html = ""
        if "contact" in sections:
            contact_html = f"""
    <!-- CONTACT SECTION -->
    <section id="contact" class="py-20 bg-zinc-900/50 border-t border-zinc-800">
      <div class="max-w-xl mx-auto px-4 text-center">
        <h2 class="text-3xl font-extrabold text-white mb-3">Initiate Project Build</h2>
        <p class="text-sm text-zinc-400 mb-8">Enter your project specifications to dispatch the Ornàment agent fleet.</p>
        <form class="space-y-4 text-left bg-zinc-950 p-6 rounded-2xl border border-zinc-800 shadow-xl">
          <div>
            <label class="block text-xs font-semibold text-zinc-400 mb-1">Your Name or Organization</label>
            <input type="text" placeholder="Engineering Lead" class="w-full p-2.5 rounded-lg bg-zinc-900 border border-zinc-800 text-white text-xs focus:outline-none focus:border-indigo-500" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-zinc-400 mb-1">Project Requirements</label>
            <textarea rows="3" placeholder="Describe the web application, tech stack, and goals..." class="w-full p-2.5 rounded-lg bg-zinc-900 border border-zinc-800 text-white text-xs focus:outline-none focus:border-indigo-500"></textarea>
          </div>
          <button type="button" class="w-full py-3 rounded-lg {palette['primary_bg']} hover:opacity-90 text-white font-bold text-xs shadow-lg transition">
            Dispatch Autonomous Agents
          </button>
        </form>
      </div>
    </section>
"""

        return f"""<!DOCTYPE html>
<html lang="en" class="dark scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Ornàment Engineer</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            bg: '#09090b',
            accent: '{palette['primary']}'
          }}
        }}
      }}
    }}
  </script>
  <style>
    body {{ background-color: #09090b; color: #f4f4f5; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
  </style>
</head>
<body class="min-h-screen bg-[#09090b] text-zinc-100 antialiased flex flex-col">
  <!-- Top Navigation -->
  <header class="sticky top-0 z-50 w-full border-b border-zinc-800 bg-[#09090b]/80 backdrop-blur-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 rounded-lg {palette['primary_bg']} flex items-center justify-center font-black text-white text-base shadow-lg shadow-[{palette['glow']}]">
          {site_type[0].upper()}
        </div>
        <span class="font-bold text-lg text-white tracking-tight">{site_type.capitalize()}<span class="{palette['primary_text']}">.ai</span></span>
      </div>
      <nav aria-label="Main Navigation" class="hidden md:flex items-center space-x-6 text-sm">
        <a href="#features" class="text-zinc-400 hover:text-white transition">Features</a>
        <a href="#stats" class="text-zinc-400 hover:text-white transition">Metrics</a>
        <a href="#pricing" class="text-zinc-400 hover:text-white transition">Pricing</a>
        <a id="nav-contact-button" href="/contact" class="px-4 py-2 rounded-full {palette['primary_bg']} hover:opacity-90 text-white font-medium text-xs transition shadow-md">
          Get in Touch
        </a>
      </nav>
    </div>
  </header>

  <!-- Page Body -->
  <main class="flex-1">
    {hero_html}
    {features_html}
    {stats_html}
    {pricing_html}
    {contact_html}
  </main>

  <!-- Footer -->
  <footer class="border-t border-zinc-800/80 py-8 bg-zinc-950 text-center text-xs text-zinc-500">
    <p>Engineered autonomously by <strong class="text-zinc-300">Ornàment AI Website Engineer</strong>. Zero runtime regressions.</p>
  </footer>
</body>
</html>"""
