from pathlib import Path
from typing import Dict, Any
from ornament.files.file_manager import FileManager

class SaasGenerator:
    """
    Scaffolds production-grade Next.js + React + TypeScript + Tailwind SaaS / Startup websites (Section 21).
    Capabilities: Hero, features, pricing table, testimonials, FAQ accordion, CTA, dashboard previews.
    """

    @classmethod
    def generate(cls, workspace_path: Path) -> Dict[str, Any]:
        fm = FileManager(workspace_path)

        # 1. package.json
        package_json = """{
  "name": "ornament-saas-platform",
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

        # 2. tsconfig.json
        tsconfig_json = """{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{"name": "next"}],
    "paths": {"@/*": ["./*"]}
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
"""
        fm.create_file("tsconfig.json", tsconfig_json, overwrite=True)

        # 3. tailwind.config.js
        tailwind_config = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "#030712",
        surface: "#111827",
        border: "#1f2937",
        accent: "#38bdf8"
      }
    },
  },
  plugins: [],
}
"""
        fm.create_file("tailwind.config.js", tailwind_config, overwrite=True)

        # 4. app/globals.css
        globals_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

:root { color-scheme: dark; }
body { background-color: #030712; color: #f9fafb; margin: 0; }
"""
        fm.create_file("app/globals.css", globals_css, overwrite=True)

        # 5. components/SaasNavbar.tsx
        navbar_tsx = """import React from "react";

export default function SaasNavbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-800 bg-[#030712]/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <a href="/" className="font-extrabold text-xl tracking-tight text-white flex items-center space-x-2">
          <span className="w-7 h-7 rounded-lg bg-sky-500 flex items-center justify-center text-sm font-black text-black">V</span>
          <span>VORTEX<span className="text-sky-400">.AI</span></span>
        </a>
        <nav aria-label="SaaS Navigation" className="hidden md:flex items-center space-x-8 text-sm font-medium">
          <a href="#features" className="text-gray-300 hover:text-white transition">Features</a>
          <a href="#pricing" className="text-gray-300 hover:text-white transition">Pricing</a>
          <a href="/dashboard-preview" className="text-gray-300 hover:text-white transition">Dashboard</a>
          <a href="#faq" className="text-gray-300 hover:text-white transition">FAQ</a>
        </nav>
        <div className="flex items-center space-x-4">
          <a
            id="nav-get-started"
            href="/pricing"
            className="px-4 py-2 rounded-lg bg-sky-500 hover:bg-sky-400 text-sm font-semibold text-black transition shadow-sm hover:shadow-sky-500/25"
          >
            Start Free Trial
          </a>
        </div>
      </div>
    </header>
  );
}
"""
        fm.create_file("components/SaasNavbar.tsx", navbar_tsx, overwrite=True)

        # 6. app/layout.tsx
        layout_tsx = """import "./globals.css";
import React from "react";
import SaasNavbar from "@/components/SaasNavbar";

export const metadata = {
  title: "Vortex AI | Autonomous Cloud & Agent Orchestration",
  description: "Next-generation distributed agent infrastructure and compiler observability.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen flex flex-col bg-background text-gray-100 antialiased">
        <SaasNavbar />
        <main className="flex-1 w-full mx-auto">
          {children}
        </main>
      </body>
    </html>
  );
}
"""
        fm.create_file("app/layout.tsx", layout_tsx, overwrite=True)

        # 7. components/PricingCards.tsx
        pricing_tsx = """import React from "react";

export default function PricingCards() {
  const tiers = [
    {
      name: "Developer",
      price: "$29",
      period: "/month",
      desc: "For individual engineers building local-first autonomous tools.",
      features: ["Up to 3 concurrent agents", "Local Qwen model provider", "Unlimited Git checkpoints", "Community support"],
      popular: false
    },
    {
      name: "Team Pro",
      price: "$99",
      period: "/month",
      desc: "For engineering teams shipping production web applications.",
      features: ["Up to 10 concurrent agents", "Shared vector RAG cluster", "Automated Playwright regression testing", "Priority email & Slack support"],
      popular: true
    },
    {
      name: "Enterprise",
      price: "Custom",
      period: "",
      desc: "Dedicated compute clusters with custom LoRA fine-tuning pipelines.",
      features: ["Unlimited sub-agent concurrency", "Air-gapped on-prem deployment", "Custom benchmark suites", "24/7 dedicated solutions architect"],
      popular: false
    }
  ];

  return (
    <section id="pricing" className="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="text-center max-w-2xl mx-auto mb-16">
        <h2 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight">Transparent, predictable pricing</h2>
        <p className="mt-4 text-gray-400 text-lg">Scale from local prototyping to distributed autonomous production fleets.</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {tiers.map((t, idx) => (
          <div
            key={idx}
            className={`p-8 rounded-2xl border ${t.popular ? 'border-sky-500 bg-gray-900/90 shadow-2xl shadow-sky-500/10' : 'border-gray-800 bg-gray-900/40'} flex flex-col justify-between`}
          >
            <div>
              {t.popular && (
                <span className="inline-block px-3 py-1 rounded-full bg-sky-500/10 text-sky-400 text-xs font-bold uppercase tracking-wider mb-4 border border-sky-500/20">
                  Most Popular
                </span>
              )}
              <h3 className="text-2xl font-bold text-white mb-2">{t.name}</h3>
              <p className="text-sm text-gray-400 mb-6">{t.desc}</p>
              <div className="flex items-baseline mb-6">
                <span className="text-4xl font-extrabold text-white">{t.price}</span>
                <span className="text-gray-400 text-sm ml-1">{t.period}</span>
              </div>
              <ul className="space-y-3 text-sm text-gray-300 mb-8">
                {t.features.map((f, fIdx) => (
                  <li key={fIdx} className="flex items-center space-x-3">
                    <span className="w-1.5 h-1.5 rounded-full bg-sky-400"></span>
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
            </div>
            <a
              href="/pricing"
              className={`w-full py-3 rounded-lg text-center font-semibold text-sm transition ${t.popular ? 'bg-sky-500 hover:bg-sky-400 text-black' : 'bg-gray-800 hover:bg-gray-700 text-white'}`}
            >
              Get Started
            </a>
          </div>
        ))}
      </div>
    </section>
  );
}
"""
        fm.create_file("components/PricingCards.tsx", pricing_tsx, overwrite=True)

        # 8. components/FAQAccordion.tsx
        faq_tsx = """import React from "react";

export default function FAQAccordion() {
  const faqs = [
    { q: "How does the Minimal Change Policy prevent regressions?", a: "Ornàment diagnoses root causes and performs targeted line-level replacements instead of regenerating entire files, preserving already validated code." },
    { q: "Can I run this on a 6GB VRAM GPU?", a: "Yes! The system automatically detects hardware telemetry, applies 4-bit quantization, and manages concurrency dynamically to run smoothly inside 6GB VRAM bounds." },
    { q: "How does Playwright browser testing integrate?", a: "Every code change is independently validated via Playwright headless Chromium across static, build, functional, responsive, and accessibility levels before git commit." }
  ];

  return (
    <section id="faq" className="py-20 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 border-t border-gray-800">
      <h2 className="text-3xl font-extrabold text-white text-center mb-12">Frequently Asked Questions</h2>
      <div className="space-y-4">
        {faqs.map((f, idx) => (
          <div key={idx} className="p-6 rounded-xl border border-gray-800 bg-gray-900/50">
            <h3 className="font-bold text-white text-lg mb-2">{f.q}</h3>
            <p className="text-sm text-gray-400 leading-relaxed">{f.a}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
"""
        fm.create_file("components/FAQAccordion.tsx", faq_tsx, overwrite=True)

        # 9. app/page.tsx (SaaS Landing Page)
        saas_home_tsx = """import React from "react";
import PricingCards from "@/components/PricingCards";
import FAQAccordion from "@/components/FAQAccordion";

export default function SaasLandingPage() {
  return (
    <div>
      {/* Hero Section */}
      <section className="py-24 sm:py-32 text-center max-w-4xl mx-auto px-4">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full border border-sky-500/30 bg-sky-500/10 text-sky-400 text-xs font-semibold uppercase tracking-wider mb-8">
          <span>Vortex Engine v1.0 Released</span>
        </div>
        <h1 className="text-5xl sm:text-7xl font-extrabold tracking-tight text-white leading-tight">
          Autonomous website engineering for modern teams.
        </h1>
        <p className="mt-6 text-xl text-gray-400 max-w-2xl mx-auto leading-relaxed">
          Orchestrate intelligent sub-agents that plan, implement, test, and repair production Next.js websites locally.
        </p>
        <div className="mt-10 flex flex-wrap justify-center gap-4">
          <a
            href="/pricing"
            className="px-8 py-3.5 rounded-lg bg-sky-500 hover:bg-sky-400 text-black font-bold transition shadow-lg shadow-sky-500/25"
          >
            Start Free Trial
          </a>
          <a
            href="/dashboard-preview"
            className="px-8 py-3.5 rounded-lg border border-gray-800 bg-gray-900 hover:bg-gray-800 text-white font-semibold transition"
          >
            Live Dashboard Preview
          </a>
        </div>
      </section>

      {/* Feature Grid */}
      <section id="features" className="py-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 border-t border-gray-800">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="p-8 rounded-2xl border border-gray-800 bg-gray-900/40">
            <div className="w-10 h-10 rounded-lg bg-sky-500/10 text-sky-400 flex items-center justify-center font-bold mb-4">01</div>
            <h3 className="text-xl font-bold text-white mb-2">Minimal Change Policy</h3>
            <p className="text-sm text-gray-400 leading-relaxed">Isolates root causes and makes surgical patches rather than rewriting projects.</p>
          </div>
          <div className="p-8 rounded-2xl border border-gray-800 bg-gray-900/40">
            <div className="w-10 h-10 rounded-lg bg-sky-500/10 text-sky-400 flex items-center justify-center font-bold mb-4">02</div>
            <h3 className="text-xl font-bold text-white mb-2">Playwright Multi-Level Tests</h3>
            <p className="text-sm text-gray-400 leading-relaxed">Independent verification across static, build, runtime, browser DOM, and A11y.</p>
          </div>
          <div className="p-8 rounded-2xl border border-gray-800 bg-gray-900/40">
            <div className="w-10 h-10 rounded-lg bg-sky-500/10 text-sky-400 flex items-center justify-center font-bold mb-4">03</div>
            <h3 className="text-xl font-bold text-white mb-2">Hardware-Aware Concurrency</h3>
            <p className="text-sm text-gray-400 leading-relaxed">Dynamically scales agent concurrency to prevent GPU VRAM and system RAM thrashing.</p>
          </div>
        </div>
      </section>

      <PricingCards />
      <FAQAccordion />
    </div>
  );
}
"""
        fm.create_file("app/page.tsx", saas_home_tsx, overwrite=True)

        # 10. app/dashboard-preview/page.tsx (Interactive Mock Dashboard Preview)
        dashboard_preview_tsx = """import React from "react";

export default function DashboardPreviewPage() {
  return (
    <div className="py-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-gray-800">
        <div>
          <h1 className="text-2xl font-bold text-white">Agent Fleet Telemetry</h1>
          <p className="text-sm text-gray-400">Live observability into autonomous compiler and test runs.</p>
        </div>
        <div className="mt-4 sm:mt-0 flex items-center space-x-3">
          <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-green-500/10 text-green-400 border border-green-500/20">
            Fleet Healthy
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="p-5 rounded-xl border border-gray-800 bg-gray-900/60">
          <span className="text-xs uppercase font-mono text-gray-400">Active Subagents</span>
          <div className="text-3xl font-extrabold text-white mt-1">2 / 2</div>
          <span className="text-xs text-sky-400 mt-2 block">Optimal 6GB VRAM Concurrency</span>
        </div>
        <div className="p-5 rounded-xl border border-gray-800 bg-gray-900/60">
          <span className="text-xs uppercase font-mono text-gray-400">Playwright Test Pass Rate</span>
          <div className="text-3xl font-extrabold text-green-400 mt-1">100.0%</div>
          <span className="text-xs text-gray-400 mt-2 block">11 / 11 test suites passed</span>
        </div>
        <div className="p-5 rounded-xl border border-gray-800 bg-gray-900/60">
          <span className="text-xs uppercase font-mono text-gray-400">Avg Repair Latency</span>
          <div className="text-3xl font-extrabold text-white mt-1">1.8s</div>
          <span className="text-xs text-gray-400 mt-2 block">Surgical 1-file patch</span>
        </div>
        <div className="p-5 rounded-xl border border-gray-800 bg-gray-900/60">
          <span className="text-xs uppercase font-mono text-gray-400">Git Checkpoint Rollbacks</span>
          <div className="text-3xl font-extrabold text-white mt-1">0</div>
          <span className="text-xs text-gray-400 mt-2 block">Zero unhandled crashes</span>
        </div>
      </div>
    </div>
  );
}
"""
        fm.create_file("app/dashboard-preview/page.tsx", dashboard_preview_tsx, overwrite=True)

        return {
            "status": "generated",
            "type": "saas",
            "files_count": len(fm.list_files(exclude_build=True))
        }
